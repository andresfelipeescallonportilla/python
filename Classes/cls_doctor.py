"""Equivalente en Python de la clase ``Classes/clsDoctor.java``."""


class clsDoctor:
    """Médico veterinario que atiende a las mascotas."""

    def __init__(self, name: str = "", licence: str = ""):
        self.name = name
        self.licence = licence

    @property
    def name(self) -> str:
        """Nombre del doctor."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value if value is not None else ""

    @property
    def licence(self) -> str:
        """Número de licencia profesional."""
        return self._licence

    @licence.setter
    def licence(self, value: str) -> None:
        self._licence = value if value is not None else ""

    def __repr__(self) -> str:
        return f"clsDoctor(name={self.name!r}, licence={self.licence!r})"
