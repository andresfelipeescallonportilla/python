"""Exportación de reportes a Excel.

Equivalente en Python del código Java que usaba **Apache POI** (``HSSFWorkbook``
para archivos ``.xls``). Aquí se usa **openpyxl**, que genera archivos
``.xlsx`` (el formato moderno de Excel); el contenido de las hojas es el mismo:
una fila de encabezado en negrita y una fila por mascota.

Dependencia: ``pip install openpyxl``
"""

import logging
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

logger = logging.getLogger(__name__)

#: Carpeta donde se guardan los reportes (la carpeta del proyecto por defecto).
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "reportes"


def _timestamp() -> str:
    """Marca de tiempo para el nombre del archivo (equivale al DateTimeFormatter)."""
    return datetime.now().strftime("%Y_%m_%d_%H-%M-%S")


def _new_workbook(sheet_title: str, headers: list):
    """Crea el libro con la hoja y la fila de encabezados en negrita."""
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = sheet_title

    header_font = Font(bold=True)
    for column, title in enumerate(headers, start=1):
        cell = sheet.cell(row=1, column=column, value=title)
        cell.font = header_font
    return workbook, sheet


def _save(workbook, prefix: str, output_dir: Path | None = None) -> Path:
    """Guarda el libro y devuelve la ruta del archivo generado."""
    directory = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{prefix}_{_timestamp()}.xlsx"
    workbook.save(path)
    return path


def export_pet_list(dog_list: list, cat_list: list,
                    output_dir: Path | None = None) -> Path:
    """Exporta perros + gatos a una hoja llamada ``Pets``."""
    headers = ["AnimalType", "Code", "Name", "Color", "Health Status", "Breed", "Pedigree"]
    workbook, sheet = _new_workbook("Pets", headers)

    row_index = 2
    for dog in dog_list:
        pedigree = "Yes" if getattr(dog, "pedigree", False) else "No"
        values = [dog.getAnimalType(), dog.code, dog.name, dog.color,
                  dog.health_status, getattr(dog, "breed", ""), pedigree]
        for column, value in enumerate(values, start=1):
            sheet.cell(row=row_index, column=column, value=value)
        row_index += 1

    for cat in cat_list:
        values = [cat.getAnimalType(), cat.code, cat.name, cat.color,
                  cat.health_status, getattr(cat, "breed", ""), None]
        for column, value in enumerate(values, start=1):
            sheet.cell(row=row_index, column=column, value=value)
        row_index += 1

    return _save(workbook, "pet_list_report_date", output_dir)


def export_dog_list(dog_list: list, output_dir: Path | None = None) -> Path:
    """Exporta solo los perros a una hoja llamada ``Dogs``."""
    headers = ["AnimalType", "Code", "Name", "Color", "Health Status", "Breed", "Pedigree"]
    workbook, sheet = _new_workbook("Dogs", headers)

    for row_index, dog in enumerate(dog_list, start=2):
        pedigree = "Yes" if getattr(dog, "pedigree", False) else "No"
        values = [dog.getAnimalType(), dog.code, dog.name, dog.color,
                  dog.health_status, getattr(dog, "breed", ""), pedigree]
        for column, value in enumerate(values, start=1):
            sheet.cell(row=row_index, column=column, value=value)

    return _save(workbook, "dog_list_report_date", output_dir)


def export_cat_list(cat_list: list, output_dir: Path | None = None) -> Path:
    """Exporta solo los gatos a una hoja llamada ``Cats``."""
    headers = ["AnimalType", "Code", "Name", "Color", "Health Status", "Breed"]
    workbook, sheet = _new_workbook("Cats", headers)

    for row_index, cat in enumerate(cat_list, start=2):
        values = [cat.getAnimalType(), cat.code, cat.name, cat.color,
                  cat.health_status, getattr(cat, "breed", "")]
        for column, value in enumerate(values, start=1):
            sheet.cell(row=row_index, column=column, value=value)

    return _save(workbook, "cat_list_report_date", output_dir)


__all__ = ["export_cat_list", "export_dog_list", "export_pet_list", "DEFAULT_OUTPUT_DIR"]
