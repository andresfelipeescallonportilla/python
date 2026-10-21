"""Equivalente en Python de la interfaz ``Interfaces/IAnimal.java`` del proyecto Java.

La interfaz original obligaba a implementar el método ``getAnimalType()``,
que devuelve el tipo de animal de la mascota ("Dog", "Cat", ...).
"""

from abc import ABC, abstractmethod


class IAnimal(ABC):
    """Contrato que deben cumplir todas las mascotas (animales)."""

    @abstractmethod
    def getAnimalType(self) -> str:
        """Devuelve el tipo de animal ("Dog", "Cat", ...)."""
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.getAnimalType()} - {self.code}"
