"""Equivalente en Python de la clase ``Model/modelCat.java``.

Contiene el CRUD (SQL) de los gatos sobre las tablas ``tb_pet`` y ``tb_cat``.

Mismas mejoras que en ``Model/model_dog.py``: columnas explícitas, borrado
transaccional con *savepoint* y resolución dinámica de la clave primaria.
"""

import logging

from Classes.cls_cat import clsCat
from Classes.cls_pet import clsPet
from Classes.cls_report_by_health_status import clsReportByHealthStatus
from Model.db_connection import connection, cursor, get_primary_key_column
from Model.db_data import DbData

logger = logging.getLogger(__name__)

TABLE_PET = "tb_pet"
TABLE_CAT = "tb_cat"


class modelCat:
    """Modelo de datos de los gatos (capa Model del MVC)."""

    def __init__(self, db_data: DbData | None = None):
        self.db_data = db_data or DbData()
        #: Último error de MySQL ocurrido (se muestra en la interfaz).
        self.last_error = ""

    def getLastError(self) -> str:
        """Devuelve el último error de MySQL (mensaje vacío si no hubo)."""
        return self.last_error

    def _fail(self, message: str, exc: Exception) -> bool:
        """Guarda el error y devuelve ``False`` (resultado de una operación fallida)."""
        self.last_error = f"{message}: {exc}"
        logger.error("%s: %s", message, exc)
        return False

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    def CreatePet(self, cat: clsCat) -> bool:
        """Inserta la mascota en ``tb_pet`` y el gato en ``tb_cat``."""
        self.last_error = ""
        try:
            with connection(self.db_data) as conn:
                with cursor(conn) as cur:
                    cur.execute(
                        "INSERT INTO tb_pet (code, name, born_year, color, health_status) "
                        "VALUES (%s, %s, %s, %s, %s)",
                        (cat.code, cat.name, cat.born_year, cat.color, cat.health_status),
                    )
                    id_pet = cur.lastrowid

                    cur.execute(
                        "INSERT INTO tb_cat (breed, id_pet) VALUES (%s, %s)",
                        (cat.breed, id_pet),
                    )
                    rows_inserted = cur.rowcount
                    conn.commit()
                    return rows_inserted > 0
        except Exception as exc:
            return self._fail("Error al crear el gato", exc)

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------
    def SearchPet(self, code: str) -> clsPet | None:
        """Busca un gato por su código. Devuelve ``None`` si no existe."""
        cat = None
        try:
            with connection(self.db_data) as conn:
                pk = get_primary_key_column(conn, TABLE_CAT, "id_cat")
                with cursor(conn) as cur:
                    cur.execute(
                        "SELECT p.id AS pet_id, p.code, p.name, p.born_year, "
                        f"p.color, p.health_status, c.{pk} AS cat_id, c.breed "
                        "FROM tb_pet AS p INNER JOIN tb_cat AS c ON p.id = c.id_pet "
                        "WHERE p.code = %s",
                        (code,),
                    )
                    row = cur.fetchone()
                    if row:
                        cat = self._build_cat(row)
        except Exception as exc:
            self._fail("Error al buscar el gato", exc)
        return cat

    def ListPet(self) -> list:
        """Devuelve la lista de todos los gatos (``tb_pet`` + ``tb_cat``)."""
        cat_list = []
        try:
            with connection(self.db_data) as conn:
                pk = get_primary_key_column(conn, TABLE_CAT, "id_cat")
                with cursor(conn) as cur:
                    cur.execute(
                        "SELECT p.id AS pet_id, p.code, p.name, p.born_year, "
                        f"p.color, p.health_status, c.{pk} AS cat_id, c.breed "
                        "FROM tb_pet AS p INNER JOIN tb_cat AS c ON p.id = c.id_pet"
                    )
                    for row in cur.fetchall():
                        cat_list.append(self._build_cat(row))
        except Exception as exc:
            self._fail("Error al listar los gatos", exc)
        return cat_list

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    def EditPet(self, cat: clsCat) -> bool:
        """Actualiza la mascota en ``tb_pet`` y el gato en ``tb_cat``."""
        self.last_error = ""
        try:
            with connection(self.db_data) as conn:
                pk = get_primary_key_column(conn, TABLE_CAT, "id_cat")
                with cursor(conn) as cur:
                    cur.execute(
                        "UPDATE tb_pet SET code = %s, name = %s, born_year = %s, "
                        "color = %s, health_status = %s WHERE id = %s",
                        (cat.code, cat.name, cat.born_year, cat.color,
                         cat.health_status, cat.petId),
                    )
                    rows_updated_pet = cur.rowcount

                    cur.execute(
                        f"UPDATE tb_cat SET breed = %s WHERE {pk} = %s",
                        (cat.breed, cat.catId),
                    )
                    rows_updated_cat = cur.rowcount
                    conn.commit()
                    return rows_updated_pet > 0 and rows_updated_cat > 0
        except Exception as exc:
            return self._fail("Error al actualizar el gato", exc)

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    def DeletePet(self, cat: clsCat) -> bool:
        """Elimina el gato y su mascota dentro de una única transacción."""
        self.last_error = ""
        try:
            with connection(self.db_data) as conn:
                pk = get_primary_key_column(conn, TABLE_CAT, "id_cat")
                with cursor(conn) as cur:
                    cur.execute("START TRANSACTION")
                    cur.execute("SAVEPOINT deletePoint")
                    try:
                        cur.execute(f"DELETE FROM tb_cat WHERE {pk} = %s", (cat.catId,))
                        rows_updated_cat = cur.rowcount

                        cur.execute("DELETE FROM tb_pet WHERE id = %s", (cat.petId,))
                        rows_updated_pet = cur.rowcount

                        cur.execute("RELEASE SAVEPOINT deletePoint")
                        conn.commit()
                        return rows_updated_pet > 0 and rows_updated_cat > 0
                    except Exception:
                        cur.execute("ROLLBACK TO SAVEPOINT deletePoint")
                        conn.rollback()
                        self._fail("Se revirtió el borrado del gato", exc)
                        return False
        except Exception as exc:
            return self._fail("Error al eliminar el gato", exc)

    # ------------------------------------------------------------------
    # REPORTES
    # ------------------------------------------------------------------
    def ListPetByHealthStatus(self) -> list:
        """Reporte de TODAS las mascotas agrupadas por estado de salud."""
        report = []
        try:
            with connection(self.db_data) as conn:
                with cursor(conn) as cur:
                    cur.execute(
                        "SELECT health_status, COUNT(health_status) AS amount "
                        "FROM tb_pet GROUP BY health_status"
                    )
                    for row in cur.fetchall():
                        report.append(clsReportByHealthStatus(
                            row.get("health_status"),
                            row.get("amount") or 0,
                        ))
        except Exception as exc:
            self._fail("Error en el reporte por estado de salud", exc)
        return report

    def ListCatByHealthStatus(self) -> list:
        """Reporte de los GATOS agrupados por estado de salud."""
        report = []
        try:
            with connection(self.db_data) as conn:
                with cursor(conn) as cur:
                    cur.execute(
                        "SELECT a.health_status, COUNT(a.health_status) AS amount "
                        "FROM (SELECT p.code, p.name, p.born_year, p.color, "
                        "p.health_status, c.breed "
                        "FROM tb_pet AS p INNER JOIN tb_cat AS c ON p.id = c.id_pet) AS a "
                        "GROUP BY a.health_status"
                    )
                    for row in cur.fetchall():
                        report.append(clsReportByHealthStatus(
                            row.get("health_status"),
                            row.get("amount") or 0,
                        ))
        except Exception as exc:
            self._fail("Error en el reporte de gatos", exc)
        return report

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    @staticmethod
    def _build_cat(row: dict) -> clsCat:
        """Construye un :class:`clsCat` a partir de una fila del ``SELECT``."""
        return clsCat(
            catId=row.get("cat_id") or 0,
            breed=row.get("breed") or "",
            petId=row.get("pet_id") or 0,
            code=row.get("code") or "",
            name=row.get("name") or "",
            born_year=row.get("born_year") or 0,
            color=row.get("color") or "",
            health_status=row.get("health_status") or "",
        )
