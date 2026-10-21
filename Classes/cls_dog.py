"""Equivalente en Python de la clase ``Classes/clsDog.java``."""

from Classes.cls_pet import clsPet


class clsDog(clsPet):
    """Mascota de tipo perro. Hereda de :class:`Classes.cls_pet.clsPet`."""

    def __init__(self, dogId: int = 0, breed: str = "", pedigree: bool = False,
                 petId: int = 0, code: str = "", name: str = "", born_year: int = 0,
                 color: str = "", health_status: str = ""):
        super().__init__(petId, code, name, born_year, color, health_status)
        self.dogId = dogId
        self.breed = breed
        self.pedigree = pedigree

    @classmethod
    def fromIds(cls, petId: int, dogId: int) -> "clsDog":
        """Constructor alternativo usado por el borrado.

        En Java existía ``clsDog(int petId, int dogId)``; en Python se usa un
        ``classmethod`` para no confundir los parámetros con el constructor
        completo (mismo comportamiento, sin ambigüedad).
        """
        return cls(dogId=dogId, breed="", pedigree=False, petId=petId)

    # ------------------------------------------------------------------
    # Comportamiento propio del perro
    # ------------------------------------------------------------------
    def WalkAround(self, km=None, dogLeash=None) -> None:
        """Camina. Equivale a las tres sobrecargas ``WalkAround`` de Java.

        - ``WalkAround()``            -> imprime que camina
        - ``WalkAround(5)``          -> imprime cuántos km camina
        - ``WalkAround(True/False)``  -> indica si camina con o sin correa
        """
        name = self.name
        if km is None and dogLeash is None:
            print(f"El perro {name} está caminando.")
        elif km is not None:
            print(f"El perro {name} está caminando {km} km")
        else:
            hasLeash = "con correa" if dogLeash else "sin correa"
            print(f"El perro {name} está caminando {hasLeash}")

    def Sound(self) -> None:
        """Ladrido (sobrescribe ``clsPet.Sound``)."""
        print(f"El perro {self.name} hace Guuuuaaaauuu")

    def getAnimalType(self) -> str:
        return "Dog"

    def getNumberOfBones(self) -> int:
        return 320

    # ------------------------------------------------------------------
    # Propiedades
    # ------------------------------------------------------------------
    @property
    def dogId(self) -> int:
        """Identificador del perro (``tb_dog.id_dog``)."""
        return self._dogId

    @dogId.setter
    def dogId(self, value: int) -> None:
        self._dogId = int(value) if value is not None else 0

    @property
    def breed(self) -> str:
        """Raza del perro (``tb_dog.breed``)."""
        return self._breed

    @breed.setter
    def breed(self, value: str) -> None:
        self._breed = value if value is not None else ""

    @property
    def pedigree(self) -> bool:
        """Indica si el perro tiene pedigrí (``tb_dog.pedigree``)."""
        return self._pedigree

    @pedigree.setter
    def pedigree(self, value) -> None:
        self._pedigree = bool(value)
