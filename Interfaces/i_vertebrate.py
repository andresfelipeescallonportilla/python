"""Equivalente en Python de la interfaz ``Interfaces/IVertebrate.java``.

La interfaz original obligaba a implementar ``getNumberOfBones()``.
"""

from abc import ABC, abstractmethod


class IVertebrate(ABC):
    """Contrato para los vertebrados."""

    @abstractmethod
    def getNumberOfBones(self) -> int:
        """Devuelve la cantidad de huesos del vertebrado."""
        raise NotImplementedError
