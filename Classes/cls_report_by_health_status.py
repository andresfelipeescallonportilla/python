"""Equivalente en Python de la clase ``Classes/clsReportByHealthStatus.java``.

Representa una fila del reporte: un estado de salud y la cantidad de mascotas
que lo tienen.
"""


class clsReportByHealthStatus:
    """Registro del reporte de mascotas agrupadas por estado de salud."""

    def __init__(self, healthStatus: str = "", amountOfPetsByHealthStatus: int = 0):
        self.health_status = healthStatus
        self.amount_of_pets_by_health_status = amountOfPetsByHealthStatus

    @property
    def health_status(self) -> str:
        """Estado de salud (Sick / Healthy / In Surgery ...)."""
        return self._health_status

    @health_status.setter
    def health_status(self, value: str) -> None:
        self._health_status = value if value is not None else ""

    @property
    def amount_of_pets_by_health_status(self) -> int:
        """Cantidad de mascotas con ese estado de salud."""
        return self._amount_of_pets_by_health_status

    @amount_of_pets_by_health_status.setter
    def amount_of_pets_by_health_status(self, value: int) -> None:
        self._amount_of_pets_by_health_status = int(value) if value is not None else 0

    def __repr__(self) -> str:
        return (f"clsReportByHealthStatus(health_status={self.health_status!r}, "
                f"amount_of_pets_by_health_status={self.amount_of_pets_by_health_status})")
