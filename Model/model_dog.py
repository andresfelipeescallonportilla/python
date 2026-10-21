"""Equivalente en Python de la clase ``Model/modelDog.java``.

Contiene el CRUD (SQL) de los perros sobre las tablas ``tb_pet`` y ``tb_dog``.

Diferencias respecto a Java (mejoras deliberadas):

* Se usan columnas explícitas en el ``SELECT`` en lugar de ``SELECT *`` con
  índices numéricos (``result.getInt(1)``), de modo que el orden de las
  columnas de la tabla no puede romper la aplicación.
* El borrado se hace dentro de una única transacción con *savepoint*
  (en Java se hacía ``commit`` entre los dos ``DELETE``, lo que anulaba la
  atomicidad que el propio comentario del código describía).
* El nombre real de la clave primaria de ``tb_dog`` se resuelve en tiempo de
  ejecución, por lo que funciona tanto con ``id_dog`` como con ``id``.
"""

import logging

from Classes.cls_dog import clsDog
from Classes.cls_pet import clsPet
from Classes.cls_report_by_health_status import clsReportByHealthStatus
from Model.db_connection import connection, cursor, get_primary_key_column
from Model.db_data import DbData

logger = logging.getLogger(__name__)

TABLE_PET = "tb_pet"
TABLE_DOG = "tb_dog"


class modelDog:
    """Modelo de datos de los perros (capa Model del MVC)."""

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
    def CreatePet(self, dog: clsDog) -> bool:
        """Inserta la mascota en ``tb_pet`` y el perro en ``tb_dog``."""
        self.last_error = ""
        try:
            with connection(self.db_data) as conn:
                with cursor(conn) as cur:
                    cur.execute(
                        "INSERT INTO tb_pet (code, name, born_year, color, health_status) "
                        "VALUES (%s, %s, %s, %s, %s)",
                        (dog.code, dog.name, dog.born_year, dog.color, dog.health_status),
                    )
                    id_pet = cur.lastrowid

                    cur.execute(
                        "INSERT INTO tb_dog (breed, pedigree, id_pet) "
                        "VALUES (%s, %s, %s)",
                        (dog.breed, dog.pedigree, id_pet),
                    )
                    rows_inserted = cur.rowcount
                    conn.commit()
                    return rows_inserted > 0
        except Exception as exc:
            return self._fail("Error al crear el perro", exc)

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------
    def SearchPet(self, code: str) -> clsPet | None:
        """Busca un perro por su código. Devuelve ``None`` si no existe."""
        dog = None
        try:
            with connection(self.db_data) as conn:
                pk = get_primary_key_column(conn, TABLE_DOG, "id_dog")
                with cursor(conn) as cur:
                    cur.execute(
                        "SELECT p.id AS pet_id, p.code, p.name, p.born_year, "
                        f"p.color, p.health_status, d.{pk} AS dog_id, d.breed, d.pedigree "
                        "FROM tb_pet AS p INNER JOIN tb_dog AS d ON p.id = d.id_pet "
                        "WHERE p.code = %s",
                        (code,),
                    )
                    row = cur.fetchone()
                    if row:
                        dog = self._build_dog(row)
        except Exception as exc:
            self._fail("Error al buscar el perro", exc)
        return dog

    def ListPet(self) -> list:
        """Devuelve la lista de todos los perros (``tb_pet`` + ``tb_dog``)."""
        dog_list = []
        try:
            with connection(self.db_data) as conn:
                pk = get_primary_key_column(conn, TABLE_DOG, "id_dog")
                with cursor(conn) as cur:
                    cur.execute(
                        "SELECT p.id AS pet_id, p.code, p.name, p.born_year, "
                        f"p.color, p.health_status, d.{pk} AS dog_id, d.breed, d.pedigree "
                        "FROM tb_pet AS p INNER JOIN tb_dog AS d ON p.id = d.id_pet"
                    )
                    for row in cur.fetchall():
                        dog_list.append(self._build_dog(row))
        except Exception as exc:
            self._fail("Error al listar los perros", exc)
        return dog_list

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    def EditPet(self, dog: clsDog) -> bool:
        """Actualiza la mascota en ``tb_pet`` y el perro en ``tb_dog``."""
        self.last_error = ""
        try:
            with connection(self.db_data) as conn:
                pk = get_primary_key_column(conn, TABLE_DOG, "id_dog")
                with cursor(conn) as cur:
                    cur.execute(
                        "UPDATE tb_pet SET code = %s, name = %s, born_year = %s, "
                        "color = %s, health_status = %s WHERE id = %s",
                        (dog.code, dog.name, dog.born_year, dog.color,
                         dog.health_status, dog.petId),
                    )
                    rows_updated_pet = cur.rowcount

                    cur.execute(
                        f"UPDATE tb_dog SET breed = %s, pedigree = %s WHERE {pk} = %s",
                        (dog.breed, dog.pedigree, dog.dogId),
                    )
                    rows_updated_dog = cur.rowcount
                    conn.commit()
                    return rows_updated_pet > 0 and rows_updated_dog > 0
        except Exception as exc:
            return self._fail("Error al actualizar el perro", exc)

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    def DeletePet(self, dog: clsDog) -> bool:
        """Elimina el perro y su mascota dentro de una única transacción.

        Se elimina primero el registro específico (``tb_dog``) y luego el
        general (``tb_pet``). Si algo falla se revierte con el *savepoint*.
        """
        self.last_error = ""
        try:
            with connection(self.db_data) as conn:
                pk = get_primary_key_column(conn, TABLE_DOG, "id_dog")
                with cursor(conn) as cur:
                    cur.execute("START TRANSACTION")
                    cur.execute("SAVEPOINT deletePoint")
                    try:
                        cur.execute(f"DELETE FROM tb_dog WHERE {pk} = %s", (dog.dogId,))
                        rows_updated_dog = cur.rowcount

                        cur.execute("DELETE FROM tb_pet WHERE id = %s", (dog.petId,))
                        rows_updated_pet = cur.rowcount

                        cur.execute("RELEASE SAVEPOINT deletePoint")
                        conn.commit()
                        return rows_updated_pet > 0 and rows_updated_dog > 0
                    except Exception:
                        cur.execute("ROLLBACK TO SAVEPOINT deletePoint")
                        conn.rollback()
                        self._fail("Se revirtió el borrado del perro", exc)
                        return False
        except Exception as exc:
            return self._fail("Error al eliminar el perro", exc)

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

    def ListDogByHealthStatus(self) -> list:
        """Reporte de los PERROS agrupados por estado de salud."""
        report = []
        try:
            with connection(self.db_data) as conn:
                with cursor(conn) as cur:
                    cur.execute(
                        "SELECT a.health_status, COUNT(a.health_status) AS amount "
                        "FROM (SELECT p.code, p.name, p.born_year, p.color, "
                        "p.health_status, d.breed, d.pedigree "
                        "FROM tb_pet AS p INNER JOIN tb_dog AS d ON p.id = d.id_pet) AS a "
                        "GROUP BY a.health_status"
                    )
                    for row in cur.fetchall():
                        report.append(clsReportByHealthStatus(
                            row.get("health_status"),
                            row.get("amount") or 0,
                        ))
        except Exception as exc:
            self._fail("Error en el reporte de perros", exc)
        return report

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    @staticmethod
    def _build_dog(row: dict) -> clsDog:
        """Construye un :class:`clsDog` a partir de una fila del ``SELECT``."""
        return clsDog(
            dogId=row.get("dog_id") or 0,
            breed=row.get("breed") or "",
            pedigree=bool(row.get("pedigree")),
            petId=row.get("pet_id") or 0,
            code=row.get("code") or "",
            name=row.get("name") or "",
            born_year=row.get("born_year") or 0,
            color=row.get("color") or "",
            health_status=row.get("health_status") or "",
        )
