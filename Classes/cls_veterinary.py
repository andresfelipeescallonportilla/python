"""Equivalente en Python de la clase ``Classes/clsVeterinary.java``."""

from Classes.abst_hospital import AbstHospital
from Classes.cls_doctor import clsDoctor


class clsVeterinary(AbstHospital):
    """Clínica veterinaria. Extiende de :class:`Classes.abst_hospital.AbstHospital`."""

    def __init__(self, name: str = "", phone: str = "", address: str = "",
                 doctor: clsDoctor = None, data: str = ""):
        super().__init__(data)
        self.name = name
        self.phone = phone
        self.address = address
        self.doctor = doctor

    def PetCare(self, pet) -> str:
        """Atiende a una mascota y devuelve su estado de salud."""
        print(f"Atendiendo a la mascota {pet.name}")
        return pet.health_status

    def getPatientType(self) -> str:
        return "Animal"

    def Surgery(self) -> str:
        return "Surgery animal data"

    # ------------------------------------------------------------------
    # Propiedades
    # ------------------------------------------------------------------
    @property
    def name(self) -> str:
        """Nombre de la clínica veterinaria."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value if value is not None else ""

    @property
    def phone(self) -> str:
        """Teléfono de la clínica."""
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        self._phone = value if value is not None else ""

    @property
    def address(self) -> str:
        """Dirección de la clínica."""
        return self._address

    @address.setter
    def address(self, value: str) -> None:
        self._address = value if value is not None else ""

    @property
    def doctor(self) -> clsDoctor:
        """Doctor asignado a la clínica."""
        return self._doctor

    @doctor.setter
    def doctor(self, value) -> None:
        self._doctor = value
