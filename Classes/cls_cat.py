"""Equivalente en Python de la clase ``Classes/clsCat.java``."""

from Classes.cls_pet import clsPet


class clsCat(clsPet):
    """Mascota de tipo gato. Hereda de :class:`Classes.cls_pet.clsPet`."""

    def __init__(self, catId: int = 0, breed: str = "", petId: int = 0,
                 code: str = "", name: str = "", born_year: int = 0,
                 color: str = "", health_status: str = ""):
        super().__init__(petId, code, name, born_year, color, health_status)
        self.catId = catId
        self.breed = breed

    @classmethod
    def fromIds(cls, petId: int, catId: int) -> "clsCat":
        """Constructor alternativo usado por el borrado (ver ``clsDog.fromIds``)."""
        return cls(catId=catId, breed="", petId=petId)

    # ------------------------------------------------------------------
    # Comportamiento propio del gato
    # ------------------------------------------------------------------
    def SelfCleaning(self) -> None:
        """El gato se limpia."""
        print(f"El gato {self.name} se está limpiando.")

    def Sound(self) -> None:
        """Maullido (sobrescribe ``clsPet.Sound``)."""
        print(f"El gato {self.name} hace miaaauuu")

    def getAnimalType(self) -> str:
        return "Cat"

    def getNumberOfBones(self) -> int:
        return 230

    # ------------------------------------------------------------------
    # Propiedades
    # ------------------------------------------------------------------
    @property
    def catId(self) -> int:
        """Identificador del gato (``tb_cat.id_cat``)."""
        return self._catId

    @catId.setter
    def catId(self, value: int) -> None:
        self._catId = int(value) if value is not None else 0

    @property
    def breed(self) -> str:
        """Raza del gato (``tb_cat.breed``)."""
        return self._breed

    @breed.setter
    def breed(self, value: str) -> None:
        self._breed = value if value is not None else ""
