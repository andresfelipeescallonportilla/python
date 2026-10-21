"""Paquete ``View`` (equivalente al paquete Java ``View``).

    - ``frm_pet.frmPet``        -> ventana principal en Tkinter (como ``frmPet.java``)
    - ``charts``                -> gráficos con matplotlib (equivalente a JFreeChart)
    - ``excel_export``          -> exportación a Excel con openpyxl (equivalente a Apache POI)

Nota: ``frm_pet`` y ``charts`` no se importan aquí de forma automática para no
cargar ``matplotlib`` cuando solo se usan el modelo o el controlador.
"""

__all__ = ["charts", "excel_export", "frm_pet"]
