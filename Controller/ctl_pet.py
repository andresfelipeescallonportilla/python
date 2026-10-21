"""Equivalente en Python de la clase ``Controller/ctlPet.java``.

El controlador es el "puente" entre la Vista (Tkinter) y el Modelo (SQL).
Mantiene la misma lógica: según el tipo de animal (``Dog`` / ``Cat``) delega la
operación en el modelo correspondiente.
"""

import logging

from Classes.cls_pet import clsPet
from Classes.cls_report_by_health_status import clsReportByHealthStatus
from Model.db_data import DbData
from Model.model_cat import modelCat
from Model.model_dog import modelDog

logger = logging.getLogger(__name__)

DOG = "Dog"
CAT = "Cat"


class ctlPet:
    """Controlador del CRUD de mascotas."""

    def __init__(self, db_data: DbData | None = None):
        self.modelDog = modelDog(db_data)   # puente entre controlador y modelo
        self.modelCat = modelCat(db_data)   # puente entre controlador y modelo

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    def CreatePet(self, pet: clsPet) -> bool:
        """Crea una mascota (perro o gato).

        Devuelve ``True`` solo si la inserción se realizó correctamente.
        (En el proyecto Java se devolvía siempre ``True``; aquí se corrige
        para que la interfaz informe del error real.)
        """
        try:
            animal_type = pet.getAnimalType()
            if animal_type == DOG:
                return self.modelDog.CreatePet(pet)
            if animal_type == CAT:
                return self.modelCat.CreatePet(pet)
            return False
        except Exception as exc:
            logger.error("Error en CreatePet: %s", exc)
            return False

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------
    def SearchPet(self, code: str, type: str) -> clsPet | None:
        """Busca una mascota por su código y tipo."""
        try:
            if type == CAT:
                return self.modelCat.SearchPet(code)
            if type == DOG:
                return self.modelDog.SearchPet(code)
            return None
        except Exception as exc:
            logger.error("Error en SearchPet: %s", exc)
            return None

    def ListPet(self, type: str) -> list:
        """Lista todas las mascotas del tipo indicado."""
        try:
            if type == DOG:
                return self.modelDog.ListPet()
            if type == CAT:
                return self.modelCat.ListPet()
            return []
        except Exception as exc:
            logger.error("Error en ListPet: %s", exc)
            return []

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    def EditPet(self, pet: clsPet) -> bool:
        """Actualiza una mascota (perro o gato).

        Devuelve ``True`` solo si la actualización se realizó correctamente.
        """
        try:
            animal_type = pet.getAnimalType()
            if animal_type == CAT:
                return self.modelCat.EditPet(pet)
            if animal_type == DOG:
                return self.modelDog.EditPet(pet)
            return False
        except Exception as exc:
            logger.error("Error en EditPet: %s", exc)
            return False

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    def DeletePet(self, pet: clsPet) -> bool:
        """Elimina una mascota (perro o gato).

        Devuelve ``True`` solo si el borrado se realizó correctamente.
        """
        try:
            animal_type = pet.getAnimalType()
            if animal_type == CAT:
                return self.modelCat.DeletePet(pet)
            if animal_type == DOG:
                return self.modelDog.DeletePet(pet)
            return False
        except Exception as exc:
            logger.error("Error en DeletePet: %s", exc)
            return False

    # ------------------------------------------------------------------
    # REPORTES
    # ------------------------------------------------------------------
    def ListPetByHealthStatus(self) -> list:
        """Mascotas (todas) agrupadas por estado de salud."""
        return self.modelCat.ListPetByHealthStatus()

    def ListDogByHealthStatus(self) -> list:
        """Perros agrupados por estado de salud."""
        return self.modelDog.ListDogByHealthStatus()

    def ListCatByHealthStatus(self) -> list:
        """Gatos agrupados por estado de salud."""
        return self.modelCat.ListCatByHealthStatus()

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def getLastError(self, type: str | None = None) -> str:
        """Devuelve el último error de MySQL registrado por los modelos.

        Sirve para mostrar en la interfaz el motivo real de un fallo
        (por ejemplo, un campo que excede el tamaño de la columna).
        """
        if type == CAT:
            return self.modelCat.getLastError()
        if type == DOG:
            return self.modelDog.getLastError()
        return self.modelCat.getLastError() or self.modelDog.getLastError()

    @staticmethod
    def _to_report(records: list) -> list:
        """Convierte filas de SQL en objetos ``clsReportByHealthStatus``."""
        return [
            clsReportByHealthStatus(row.get("health_status"), row.get("amount") or 0)
            for row in records
        ]
