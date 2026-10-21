"""Equivalente en Python de la clase abstracta ``Classes/AbstHospital.java``.

En Java era una clase abstracta con métodos abstractos ``getPatientType()`` y
``Surgery()``; en Python se usa ``abc.ABC`` con ``@abstractmethod``.
"""

from abc import ABC, abstractmethod


class AbstHospital(ABC):
    """Clase base abstracta para los hospitales / clínicas veterinarias."""

    def __init__(self, data: str = ""):
        self.data = data

    @abstractmethod
    def getPatientType(self) -> str:
        """Tipo de paciente que atiende la clínica."""
        raise NotImplementedError

    @abstractmethod
    def Surgery(self) -> str:
        """Descripción del servicio de cirugía."""
        raise NotImplementedError

    def getHospitalInformation(self) -> str:
        """Devuelve la información del hospital."""
        return f"La información es: {self.getData()}"

    # ------------------------------------------------------------------
    # Propiedades
    # ------------------------------------------------------------------
    @property
    def data(self) -> str:
        """Datos informative del hospital."""
        return self._data

    @data.setter
    def data(self, value: str) -> None:
        self._data = value if value is not None else ""

    def getData(self) -> str:
        """Acceso equivalente a ``getData()`` de Java."""
        return self.data

    def setData(self, value: str) -> None:
        """Acceso equivalente a ``setData()`` de Java."""
        self.data = value
