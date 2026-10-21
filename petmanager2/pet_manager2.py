"""Equivalente en Python de la clase ``petmanager2/PetManager2.java``.

En Java esta clase estaba vacía (solo el ``main`` generado por NetBeans) y la
interfaz se lanzaba desde ``frmPet.main``. Aquí la clase es el punto de
entrada real de la aplicación: crea la ventana y la muestra.
"""

import logging

from View.frm_pet import frmPet


class PetManager2:
    """Aplicación Pet Manager (punto de entrada)."""

    def __init__(self, db_data=None):
        self.logger = logging.getLogger(__name__)
        self.db_data = db_data
        self.window = None

    def run(self) -> None:
        """Crea la ventana y entra en el bucle de eventos de Tkinter."""
        self.window = frmPet(self.db_data)
        self.window.mainloop()


def main() -> None:
    """Función ``main`` equivalente a la de Java."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    PetManager2().run()


if __name__ == "__main__":
    main()
