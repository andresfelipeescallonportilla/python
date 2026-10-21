"""Punto de entrada rápido del proyecto Python Pet Manager.

Ejemplos::

    python main.py
    python -m petmanager2.pet_manager2

Desde Visual Studio Code: botón *Run Python File* sobre este archivo, o
``F5`` con el archivo ``main.py`` como punto de entrada.
"""

import sys
from pathlib import Path

# Permite ejecutar el proyecto desde cualquier carpeta (p. ej. desde VS Code
# con un ``cwd`` diferente al del script).
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from petmanager2.pet_manager2 import main  # noqa: E402

if __name__ == "__main__":
    main()
