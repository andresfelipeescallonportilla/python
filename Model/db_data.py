"""Equivalente en Python de la clase ``Model/DbData.java``.

En Java, la clase ``DbData`` guardaba los datos de conexión (driver, usuario,
password y URL JDBC) y el modelo los usaba con
``DriverManager.getConnection(dbData.getUrl(), ...)``.

En Python no existe el concepto de "driver JDBC" como archivo ``.jar`` que haya
que copiar a una carpeta de librerías: el equivalente es un **paquete de
Python** que se instala con ``pip`` (por ejemplo ``mysql-connector-python``,
que es el conector oficial de MySQL para Python, o ``PyMySQL``).

Los valores de conexión se pueden dejar en los valores por defecto (XAMPP:
``localhost:3306``, usuario ``root`` y contraseña vacía) o personalizarlos con
variables de entorno / un archivo ``.env``.
"""

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Valores por defecto (XAMPP / phpMyAdmin en local)
# ---------------------------------------------------------------------------
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 3306
DEFAULT_USER = "root"
DEFAULT_PASSWORD = ""
DEFAULT_DATABASE = "gestormascotasbd"

#: Nombre del paquete que se usa como "driver" (el equivalente al .jar de Java).
DEFAULT_DRIVER = "mysql-connector-python"


def load_dotenv(path: Path | str | None = None) -> dict:
    """Carga un archivo ``.env`` sin dependencias externas.

    Formato soportado::

        DB_HOST=localhost
        DB_PORT=3306
        DB_USER=root
        DB_PASSWORD=
        DB_NAME=gestormascotasbd

    Las variables ya definidas en el entorno tienen prioridad (no se pisan).
    """
    if path is None:
        path = Path(__file__).resolve().parent.parent / ".env"
    path = Path(path)
    values = {}
    if not path.is_file():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        values[key] = value
        os.environ.setdefault(key, value)
    return values


class DbData:
    """Datos de conexión con la base de datos MySQL ``gestormascotasbd``."""

    def __init__(self, host: str | None = None, port: int | None = None,
                 user: str | None = None, password: str | None = None,
                 database: str | None = None):
        load_dotenv()

        self.host = host if host is not None else os.getenv("DB_HOST", DEFAULT_HOST)
        self.port = int(port if port is not None else os.getenv("DB_PORT", DEFAULT_PORT))
        self.user = user if user is not None else os.getenv("DB_USER", DEFAULT_USER)
        # OJO: la contraseña vacía es válida en XAMPP, por eso se comprueba None.
        self.password = (password if password is not None
                         else os.getenv("DB_PASSWORD", DEFAULT_PASSWORD))
        self.database = (database if database is not None
                         else os.getenv("DB_NAME", DEFAULT_DATABASE))

    # ------------------------------------------------------------------
    # Propiedades equivalentes a los getters de Java
    # ------------------------------------------------------------------
    @property
    def driver(self) -> str:
        """Paquete de Python usado como driver MySQL."""
        return os.getenv("DB_DRIVER", DEFAULT_DRIVER)

    @property
    def url(self) -> str:
        """URL de la base de datos (formato ``mysql://host:port/base``)."""
        return f"mysql://{self.host}:{self.port}/{self.database}"

    @property
    def jdbc_url(self) -> str:
        """URL equivalente a la de Java (solo informativa / migración)."""
        return (f"jdbc:mysql://{self.host}:{self.port}/{self.database}"
                "?useSSL=false&allowPublicKeyRetrieval=true")

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def getUrl(self) -> str:
        """Acceso equivalente a ``DbData.getUrl()`` de Java."""
        return self.url

    def getUser(self) -> str:
        """Acceso equivalente a ``DbData.getUser()`` de Java."""
        return self.user

    def getPassword(self) -> str:
        """Acceso equivalente a ``DbData.getPassword()`` de Java."""
        return self.password

    def getDriver(self) -> str:
        """Acceso equivalente a ``DbData.getDriver()`` de Java."""
        return self.driver

    def __repr__(self) -> str:
        return (f"DbData(host={self.host!r}, port={self.port}, user={self.user!r}, "
                f"database={self.database!r})")
