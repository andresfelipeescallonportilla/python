"""Capa de conexión MySQL para Python (equivalente a ``DriverManager`` de Java).

En Java la conexión se hacía así::

    Class.forName("com.mysql.jdbc.Driver");
    Connection conn = DriverManager.getConnection(url, user, password);

En Python el "driver" es un paquete instalado con ``pip``. Este módulo abstrae
el driver para que el resto del código no tenga que inquietar por cuál se está
usando:

* ``mysql-connector-python`` -> conector oficial de MySQL (el equivalente
  directo de ``mysql-connector-java``).
* ``PyMySQL``                -> alternativa 100 % Python (sin compilación).

Ambos usan ``%s`` como marcador de parámetros (igual que los ``?`` de JDBC) y
soportan transacciones y *savepoints*.

Instalación::

    pip install mysql-connector-python      # o: pip install pymysql
"""

import logging
from contextlib import contextmanager

from Model.db_data import DbData

logger = logging.getLogger(__name__)


class DatabaseConnectionError(Exception):
    """Error al conectar con la base de datos MySQL."""


class DriverNotInstalledError(DatabaseConnectionError):
    """No hay ningún driver MySQL instalado en el entorno de Python."""


# ---------------------------------------------------------------------------
# Cache de la clave primaria real de las tablas hijas.
# El proyecto Java usaba nombres inconsistentes ("id" en el DELETE y
# "id_cat"/"id_dog" en el UPDATE). Aquí se resuelve dinámicamente leyendo
# INFORMATION_SCHEMA, así el programa funciona con cualquiera de las dos
# nomenclaturas sin tocar el código.
# ---------------------------------------------------------------------------
_PRIMARY_KEY_CACHE: dict = {}


def get_connection(db_data: DbData | None = None):
    """Abre una conexión con MySQL.

    Equivale a ``DriverManager.getConnection(url, user, password)`` de Java.
    """
    db_data = db_data or DbData()

    # 1) mysql-connector-python (conector oficial de MySQL)
    try:
        import mysql.connector
        from mysql.connector.constants import ClientFlag
    except ImportError:
        pass
    else:
        try:
            return mysql.connector.connect(
                host=db_data.host,
                port=db_data.port,
                user=db_data.user,
                password=db_data.password,
                database=db_data.database,
                autocommit=False,
                # FOUND_ROWS: ``rowcount`` devuelve las filas *encontradas* y no
                # solo las cambiadas. Si no, guardar un registro sin modificarlo
                # devolvería 0 y la interfaz lo mostraría como error.
                client_flags=[ClientFlag.FOUND_ROWS],
            )
        except Exception as exc:  # pragma: no cover - depende del entorno
            raise DatabaseConnectionError(
                f"No se pudo conectar a MySQL en {db_data.host}:{db_data.port} "
                f"con la base de datos '{db_data.database}'.\n"
                f"Detalle: {exc}\n"
                f"Verifica que XAMPP (MySQL) esté iniciado, que el usuario "
                f"'{db_data.user}' exista en phpMyAdmin y que la contraseña sea correcta."
            ) from exc

    # 2) PyMySQL (alternativa pura en Python)
    try:
        import pymysql
    except ImportError as exc:
        raise DriverNotInstalledError(
            "Falta el driver de MySQL para Python.\n"
            "Instala uno de los dos con:\n"
            "    pip install mysql-connector-python\n"
            "o bien:\n"
            "    pip install pymysql"
        ) from exc

    try:
        return pymysql.connect(
            host=db_data.host,
            port=db_data.port,
            user=db_data.user,
            password=db_data.password,
            database=db_data.database,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
            client_flag=pymysql.constants.CLIENT.FOUND_ROWS,
        )
    except Exception as exc:  # pragma: no cover - depende del entorno
        raise DatabaseConnectionError(
            f"No se pudo conectar a MySQL en {db_data.host}:{db_data.port} "
            f"con la base de datos '{db_data.database}'.\n"
            f"Detalle: {exc}"
        ) from exc


def create_cursor(conn):
    """Crea un cursor que devuelve las filas como diccionarios.

    Equivale a ``PreparedStatement`` + ``ResultSet`` de Java, pero con acceso
    por nombre de columna (``fila["code"]``), que es más seguro que por índice.
    """
    try:
        import mysql.connector

        if isinstance(conn, mysql.connector.MySQLConnection):
            return conn.cursor(dictionary=True)
    except ImportError:
        pass

    import pymysql

    return conn.cursor(pymysql.cursors.DictCursor)


@contextmanager
def connection(db_data: DbData | None = None):
    """Context manager que abre y cierra la conexión."""
    conn = get_connection(db_data)
    try:
        yield conn
    finally:
        try:
            conn.close()
        except Exception:  # pragma: no cover
            logger.debug("Error al cerrar la conexión", exc_info=True)


@contextmanager
def cursor(conn):
    """Context manager que crea y cierra un cursor con filas como diccionario."""
    cur = create_cursor(conn)
    try:
        yield cur
    finally:
        try:
            cur.close()
        except Exception:  # pragma: no cover
            logger.debug("Error al cerrar el cursor", exc_info=True)


def get_primary_key_column(conn, table: str, default: str = "id") -> str:
    """Devuelve el nombre real de la clave primaria de ``table``.

    Lee ``INFORMATION_SCHEMA`` y cachea el resultado. Si la tabla no tiene
    clave primaria devuelve ``default``.
    """
    key = (table, default)
    if key in _PRIMARY_KEY_CACHE:
        return _PRIMARY_KEY_CACHE[key]

    column = default
    try:
        with cursor(conn) as cur:
            cur.execute(
                "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
                "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s "
                "AND CONSTRAINT_NAME = 'PRIMARY'",
                (table,),
            )
            row = cur.fetchone()
            if row:
                value = row.get("COLUMN_NAME") if isinstance(row, dict) else row[0]
                if value:
                    column = value
    except Exception:  # pragma: no cover - si falla, se usa el valor por defecto
        logger.debug("No se pudo leer la clave primaria de %s", table, exc_info=True)

    _PRIMARY_KEY_CACHE[key] = column
    return column


def test_connection(db_data: DbData | None = None) -> tuple:
    """Prueba la conexión y devuelve ``(ok, mensaje)``.

    Se usa desde el botón "Test connection" de la interfaz.
    """
    db_data = db_data or DbData()
    try:
        with connection(db_data) as conn:
            with cursor(conn) as cur:
                cur.execute("SELECT VERSION() AS version, DATABASE() AS db")
                row = cur.fetchone()
                version = row.get("version") if isinstance(row, dict) else row[0]
                db_name = row.get("db") if isinstance(row, dict) else row[1]
        return True, (f"Conexión correcta a '{db_name}' "
                      f"(MySQL {version}) en {db_data.host}:{db_data.port}")
    except Exception as exc:
        return False, str(exc)
