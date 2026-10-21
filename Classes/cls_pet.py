"""Equivalente en Python de la clase ``Classes/clsPet.java``.

``clsPet`` es la clase base de todas las mascotas. En Java implementaba las
interfaces ``IAnimal`` e ``IVertebrate``; aquí se mantiene exactamente el mismo
contrato polimórfico.

Los atributos que en Java se accedían con ``getX()`` / ``setX()`` se expone aquí
como *properties* de Python (``pet.code``, ``pet.name`` ...).
"""

from Interfaces.i_animal import IAnimal
from Interfaces.i_vertebrate import IVertebrate


class clsPet(IAnimal, IVertebrate):
    """Mascota genérica (superclase de ``clsDog`` y ``clsCat``)."""

    def __init__(self, petId: int = 0, code: str = "", name: str = "",
                 born_year: int = 0, color: str = "", health_status: str = ""):
        self.petId = petId
        self.code = code
        self.name = name
        self.born_year = born_year
        self.color = color
        self.health_status = health_status
        self.veterinary = None  # type: clsVeterinary | None

    # ------------------------------------------------------------------
    # Comportamiento (equivalente a los métodos Eat/Move/Sound de Java)
    # ------------------------------------------------------------------
    def Eat(self) -> None:
        print(f"La mascota {self.name} está comiendo.")

    def Move(self) -> None:
        print(f"La mascota {self.name} está moviéndose.")

    def Sound(self) -> None:
        print(f"La mascota {self.name} está relaizando el sonido.")

    # ------------------------------------------------------------------
    # Propiedades
    # ------------------------------------------------------------------
    @property
    def petId(self) -> int:
        """Identificador de la mascota (``tb_pet.id``)."""
        return self._petId

    @petId.setter
    def petId(self, value: int) -> None:
        self._petId = int(value) if value is not None else 0

    @property
    def code(self) -> str:
        """Código de la mascota (``tb_pet.code``)."""
        return self._code

    @code.setter
    def code(self, value: str) -> None:
        self._code = value if value is not None else ""

    @property
    def name(self) -> str:
        """Nombre de la mascota (``tb_pet.name``)."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value if value is not None else ""

    @property
    def born_year(self) -> int:
        """Año de nacimiento (``tb_pet.born_year``)."""
        return self._born_year

    @born_year.setter
    def born_year(self, value: int) -> None:
        self._born_year = int(value) if value is not None else 0

    @property
    def color(self) -> str:
        """Color de la mascota (``tb_pet.color``)."""
        return self._color

    @color.setter
    def color(self, value: str) -> None:
        self._color = value if value is not None else ""

    @property
    def health_status(self) -> str:
        """Estado de salud de la mascota (``tb_pet.health_status``)."""
        return self._health_status

    @health_status.setter
    def health_status(self, value: str) -> None:
        self._health_status = value if value is not None else ""

    @property
    def veterinary(self):
        """Veterinario asignado a la mascota (``clsVeterinary``)."""
        return self._veterinary

    @veterinary.setter
    def veterinary(self, value) -> None:
        self._veterinary = value

    # ------------------------------------------------------------------
    # Contratos de las interfaces
    # ------------------------------------------------------------------
    def getAnimalType(self) -> str:
        """Tipo genérico de mascota."""
        return "Pet"

    def getNumberOfBones(self) -> int:
        """Una mascota genérica no define cantidad de huesos."""
        return 0

    def __repr__(self) -> str:
        return (f"{type(self).__name__}(petId={self.petId}, code={self.code!r}, "
                f"name={self.name!r}, born_year={self.born_year}, "
                f"color={self.color!r}, health_status={self.health_status!r})")
