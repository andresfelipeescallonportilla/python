"""Paquete ``Interfaces`` (equivalente al paquete Java ``Interfaces``).

Contiene los contratos (interfaces) que implementan las clases de ``Classes``:
    - ``i_animal.IAnimal``
    - ``i_vertebrate.IVertebrate``
"""

from .i_animal import IAnimal
from .i_vertebrate import IVertebrate

__all__ = ["IAnimal", "IVertebrate"]
