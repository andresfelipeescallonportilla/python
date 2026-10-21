"""Equivalente en Python de la vista ``View/frmPet.java``.

La ventana Swing (``JFrame``) se reemplaza por una aplicación **Tkinter**
(``tkinter.Tk`` + ``ttk.Notebook``) que mantiene la misma estructura:

============  ==========================================================
Java (Swing)  Python (Tkinter)
============  ==========================================================
``JFrame``    ``class frmPet(tkinter.Tk)``
``JTabbedPane``  ``ttk.Notebook``
``JTextField``   ``ttk.Entry``
``JComboBox``    ``ttk.Combobox``
``JCheckBox``    ``ttk.Checkbutton``
``JList``        ``ttk.Treeview``
``JOptionPane``  ``tkinter.messagebox``
``ChartPanel``   ``View.charts.ChartFrame`` (matplotlib)
============  ==========================================================

Pestañas: Pet List | Dog Manager | Cat Manager | Dog List | Cat List |
Report By Health Status | Dog Report | Cat Report
"""

import logging
import tkinter as tk
from tkinter import messagebox, ttk

from Classes.cls_cat import clsCat
from Classes.cls_dog import clsDog
from Controller.ctl_pet import ctlPet
from Model.db_connection import test_connection
from Model.db_data import DbData
from View.charts import ChartFrame, build_bar_figure, build_pie_figure
from View.excel_export import export_cat_list, export_dog_list, export_pet_list

logger = logging.getLogger(__name__)

#: Estados de salud disponibles (combos de la GUI).
HEALTH_STATUS = ["Sick", "Healthy", "In Surgery"]
#: Razas de perros (combo de la GUI).
DOG_BREEDS = ["Criollo", "Schnauzer", "German shepherd", "Pincher"]
#: Razas de gatos (combo de la GUI).
CAT_BREEDS = ["Birman", "British", "Bombay", "Abyssinian"]


class frmPet(tk.Tk):
    """Ventana principal del Pet Manager."""

    def __init__(self, db_data: DbData | None = None):
        super().__init__()

        self.title("Pet Manager")
        self.geometry("1120x700")
        self.minsize(940, 580)

        # --- Controlador (puente entre la vista y el modelo) -------------
        self.db_data = db_data or DbData()
        self.ctlPet = ctlPet(self.db_data)

        # --- Listas en memoria (como las LinkedList de Java) -------------
        self.dogObjectList: list = []
        self.catObjectList: list = []

        # --- Variables de los campos de texto ----------------------------
        self.txtCodeDog = tk.StringVar()
        self.txtNameDog = tk.StringVar()
        self.txtBornYearDog = tk.StringVar()
        self.txtColorDog = tk.StringVar()
        self.txtPetId = tk.StringVar()
        self.txtDogId = tk.StringVar()

        self.txtCodeCat = tk.StringVar()
        self.txtNameCat = tk.StringVar()
        self.txtBornYearCat = tk.StringVar()
        self.txtColorCat = tk.StringVar()
        self.txtPetId2 = tk.StringVar()
        self.txtCatId = tk.StringVar()

        self.cbBreedDog = tk.StringVar(value=DOG_BREEDS[0])
        self.cbHealthStatusDog = tk.StringVar(value=HEALTH_STATUS[0])
        self.cbPedigree = tk.BooleanVar(value=False)

        self.cbBreedCat = tk.StringVar(value=CAT_BREEDS[0])
        self.cbHealthStatusCat = tk.StringVar(value=HEALTH_STATUS[0])

        self._build_ui()
        self.load_data()

    # ==================================================================
    # CONSTRUCCIÓN DE LA INTERFAZ
    # ==================================================================
    def _build_ui(self) -> None:
        """Crea todos los widgets (equivalente a ``initComponents()`` de Java)."""
        # OJO: el orden de los ``pack`` importa. La barra de estado y la
        # cabecera se empaquetan ANTES que el notebook (que ocupa todo el
        # espacio restante con ``fill="both", expand=True``).
        self._build_status_bar()
        self._build_header()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=(0, 4))

        # 1) Pet List
        self.petList = self._build_tree_tab(self.notebook, "Pet List")
        # 2) Dog Manager
        self._build_dog_tab(self.notebook)
        # 3) Cat Manager
        self._build_cat_tab(self.notebook)
        # 4) Dog List
        self.dogList = self._build_tree_tab(self.notebook, "Dog List")
        # 5) Cat List
        self.catList = self._build_tree_tab(self.notebook, "Cat List")
        # 6-8) Reportes
        self._build_report_tabs(self.notebook)

    def _build_header(self) -> None:
        """Encabezado: título y botones de exportación (como en el ``JFrame``)."""
        header = ttk.Frame(self)
        header.pack(fill="x", padx=8, pady=(8, 4))

        ttk.Label(header, text="Pet Manager",
                  font=("Segoe UI", 22, "bold")).pack(side="left")

        buttons = ttk.Frame(header)
        buttons.pack(side="right")

        ttk.Button(buttons, text="Export Pet List",
                   command=self.btnExportarPetListActionPerformed).pack(side="left", padx=4)
        ttk.Button(buttons, text="Export Dog List",
                   command=self.btnExportarDogListActionPerformed).pack(side="left", padx=4)
        ttk.Button(buttons, text="Export Cat List",
                   command=self.btnExportarCatListActionPerformed).pack(side="left", padx=4)
        ttk.Button(buttons, text="Restart",
                   command=self.btnRestartActionPerformed).pack(side="left", padx=4)
        ttk.Button(buttons, text="Test connection",
                   command=self.btnTestConnectionActionPerformed).pack(side="left", padx=4)

    def _build_tree_tab(self, parent, title: str):
        """Crea una pestaña con un ``ttk.Treeview`` (equivalente al ``JList``)."""
        frame = ttk.Frame(parent)
        columns = ("code", "name", "type")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
        tree.heading("code", text="Code")
        tree.heading("name", text="Name")
        tree.heading("type", text="Type")
        tree.column("code", width=140, anchor="center")
        tree.column("name", width=220, anchor="w")
        tree.column("type", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        parent.add(frame, text=title)
        return tree

    def _build_dog_tab(self, parent) -> None:
        """Pestaña "Dog Manager": formulario del perro + botones CRUD."""
        frame = ttk.LabelFrame(parent, text="Dog Manager", padding=12)
        parent.add(frame, text="Dog Manager")

        grid = ttk.Frame(frame)
        grid.pack(fill="both", expand=True)
        for column, weight in ((1, 1), (3, 1)):
            grid.columnconfigure(column, weight=weight)

        entries = [
            ("Code", self.txtCodeDog, "entry"),
            ("Name", self.txtNameDog, "entry"),
            ("Born year", self.txtBornYearDog, "entry"),
            ("Color", self.txtColorDog, "entry"),
            ("Health Status", self.cbHealthStatusDog, "combo_health_dog"),
            ("Breed", self.cbBreedDog, "combo_breed_dog"),
            ("Pedigree", self.cbPedigree, "check"),
            ("petId", self.txtPetId, "entry"),
            ("dogId", self.txtDogId, "entry"),
        ]

        for index, (label, variable, kind) in enumerate(entries):
            row, column = divmod(index, 2)
            base_column = column * 2
            ttk.Label(grid, text=label).grid(row=row, column=base_column,
                                             sticky="e", padx=(0, 6), pady=5)
            if kind == "entry":
                widget = ttk.Entry(grid, textvariable=variable, width=22)
            elif kind == "check":
                widget = ttk.Checkbutton(grid, variable=variable)
            elif kind == "combo_health_dog":
                widget = ttk.Combobox(grid, textvariable=variable,
                                      values=HEALTH_STATUS, state="readonly", width=20)
            else:
                widget = ttk.Combobox(grid, textvariable=variable,
                                      values=DOG_BREEDS, state="readonly", width=20)
            widget.grid(row=row, column=base_column + 1, sticky="w", padx=(0, 18), pady=5)

        buttons = ttk.Frame(frame)
        buttons.pack(anchor="w", pady=(14, 0))
        ttk.Button(buttons, text="Save", width=12,
                   command=self.btnCrearDogActionPerformed).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Search", width=12,
                   command=self.btnBuscarDogActionPerformed).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Edit", width=12,
                   command=self.btnEditarDogActionPerformed).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Delete", width=12,
                   command=self.btnEliminarDogActionPerformed).pack(side="left")

    def _build_cat_tab(self, parent) -> None:
        """Pestaña "Cat Manager": formulario del gato + botones CRUD."""
        frame = ttk.LabelFrame(parent, text="Cat Manager", padding=12)
        parent.add(frame, text="Cat Manager")

        grid = ttk.Frame(frame)
        grid.pack(fill="both", expand=True)
        for column, weight in ((1, 1), (3, 1)):
            grid.columnconfigure(column, weight=weight)

        entries = [
            ("Code", self.txtCodeCat, "entry"),
            ("Name", self.txtNameCat, "entry"),
            ("Born year", self.txtBornYearCat, "entry"),
            ("Color", self.txtColorCat, "entry"),
            ("Health Status", self.cbHealthStatusCat, "combo_health_cat"),
            ("Breed", self.cbBreedCat, "combo_breed_cat"),
            ("petId", self.txtPetId2, "entry"),
            ("catId", self.txtCatId, "entry"),
        ]

        for index, (label, variable, kind) in enumerate(entries):
            row, column = divmod(index, 2)
            base_column = column * 2
            ttk.Label(grid, text=label).grid(row=row, column=base_column,
                                             sticky="e", padx=(0, 6), pady=5)
            if kind == "entry":
                widget = ttk.Entry(grid, textvariable=variable, width=22)
            elif kind == "combo_health_cat":
                widget = ttk.Combobox(grid, textvariable=variable,
                                      values=HEALTH_STATUS, state="readonly", width=20)
            else:
                widget = ttk.Combobox(grid, textvariable=variable,
                                      values=CAT_BREEDS, state="readonly", width=20)
            widget.grid(row=row, column=base_column + 1, sticky="w", padx=(0, 18), pady=5)

        buttons = ttk.Frame(frame)
        buttons.pack(anchor="w", pady=(14, 0))
        ttk.Button(buttons, text="Save", width=12,
                   command=self.btnCrearCatActionPerformed).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Search", width=12,
                   command=self.btnBuscarCatActionPerformed).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Edit", width=12,
                   command=self.btnEditarCatActionPerformed).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Delete", width=12,
                   command=self.btnEliminarCatActionPerformed).pack(side="left")

    def _build_report_tabs(self, parent) -> None:
        """Las tres pestañas de reportes (gráficos con matplotlib)."""
        # Report By Health Status (gráfico circular)
        frame = ttk.Frame(parent)
        parent.add(frame, text="Report By Health Status")
        # El botón se empaqueta ANTES que el gráfico (side="bottom") para que
        # quede visible debajo del canvas.
        ttk.Button(frame, text="Refresh Reports",
                   command=self.btnRefreshReportsActionPerformed).pack(
                       anchor="e", side="bottom", padx=6, pady=4)
        self.chart_pet = ChartFrame(frame)

        # Dog Report (gráfico de barras vertical)
        frame = ttk.Frame(parent)
        parent.add(frame, text="Dog Report")
        self.chart_dog = ChartFrame(frame)

        # Cat Report (gráfico de barras horizontal)
        frame = ttk.Frame(parent)
        parent.add(frame, text="Cat Report")
        self.chart_cat = ChartFrame(frame)

    def _build_status_bar(self) -> None:
        """Barra de estado inferior (muestra el estado de la conexión)."""
        bar = ttk.Frame(self)
        bar.pack(fill="x", side="bottom", padx=8, pady=(0, 6))
        self.lbl_status = ttk.Label(bar, text="", relief="sunken", anchor="w")
        self.lbl_status.pack(fill="x")

    # ==================================================================
    # DATOS
    # ==================================================================
    def load_data(self) -> None:
        """Carga las listas y los reportes desde la base de datos."""
        self.dogObjectList = self.ctlPet.ListPet("Dog")
        self.catObjectList = self.ctlPet.ListPet("Cat")
        self.FillDogJlist()
        self.FillCatJlist()
        self.FillJlist()
        self.RefreshReportByHealthStatus()
        self.RefreshDogReport()
        self.RefreshCatReport()

    def _set_status(self, message: str, error: bool = False) -> None:
        """Actualiza la barra de estado."""
        self.lbl_status.configure(text=message,
                                  foreground="#c0392b" if error else "#2c3e50")

    # ------------------------------------------------------------------
    # Rellenado de las listas (equivalente a FillJlist / FillDogJlist / ...)
    # ------------------------------------------------------------------
    def FillJlist(self) -> None:
        """Llena la lista de todas las mascotas (perros + gatos)."""
        rows = []
        for pet in list(self.dogObjectList) + list(self.catObjectList):
            rows.append((pet.code, pet.name, pet.getAnimalType()))
        self._fill_tree(self.petList, rows)

    def FillDogJlist(self) -> None:
        """Llena la lista de perros."""
        rows = [(pet.code, pet.name, pet.getAnimalType()) for pet in self.dogObjectList]
        self._fill_tree(self.dogList, rows)

    def FillCatJlist(self) -> None:
        """Llena la lista de gatos."""
        rows = [(pet.code, pet.name, pet.getAnimalType()) for pet in self.catObjectList]
        self._fill_tree(self.catList, rows)

    @staticmethod
    def _fill_tree(tree, rows) -> None:
        """Vuelca las filas en el ``Treeview``."""
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert("", "end", values=row)

    # ------------------------------------------------------------------
    # Reportes (equivalente a RefreshReportByHealthStatus / ...)
    # ------------------------------------------------------------------
    def RefreshReportByHealthStatus(self) -> None:
        """Gráfico circular: todas las mascotas por estado de salud."""
        report = self.ctlPet.ListPetByHealthStatus()
        figure = build_pie_figure(report, "Pets Classification By health status")
        self.chart_pet.set_figure(figure)

    def RefreshDogReport(self) -> None:
        """Gráfico de barras vertical: perros por estado de salud."""
        report = self.ctlPet.ListDogByHealthStatus()
        figure = build_bar_figure(report, "Dogs Classification By health status",
                                  "Health Status", "Amount of Dogs", "vertical")
        self.chart_dog.set_figure(figure)

    def RefreshCatReport(self) -> None:
        """Gráfico de barras horizontal: gatos por estado de salud."""
        report = self.ctlPet.ListCatByHealthStatus()
        figure = build_bar_figure(report, "Cats Classification By health status",
                                  "Health Status", "Amount Of Cats", "horizontal")
        self.chart_cat.set_figure(figure)

    def _refresh_all_reports(self) -> None:
        """Refresca los tres gráficos (sin mostrar diálogos, como en Java)."""
        self.RefreshReportByHealthStatus()
        self.RefreshDogReport()
        self.RefreshCatReport()

    # ==================================================================
    # CRUD - PERROS
    # ==================================================================
    def btnCrearDogActionPerformed(self) -> None:
        """Guarda un perro nuevo."""
        code = self.txtCodeDog.get().strip()
        name = self.txtNameDog.get().strip()
        color = self.txtColorDog.get().strip()

        if not code or not name or not color:
            messagebox.showinfo("Pet Manager", "Fill all fields", parent=self)
            return

        try:
            born_year = int(self.txtBornYearDog.get().strip())
        except ValueError:
            messagebox.showinfo("Pet Manager", "Please add a valid born year", parent=self)
            return

        breed = self.cbBreedDog.get()
        health_status = self.cbHealthStatusDog.get()
        pedigree = self.cbPedigree.get()

        dog = clsDog(dogId=0, breed=breed, pedigree=pedigree, petId=0, code=code,
                     name=name, born_year=born_year, color=color,
                     health_status=health_status)

        if self.ctlPet.CreatePet(dog):
            self.dogObjectList = self.ctlPet.ListPet("Dog")
            self.FillDogJlist()
            self.FillJlist()
            self.clearDogFields()
            self._refresh_all_reports()
            messagebox.showinfo("Pet Manager", "The record has been saved", parent=self)
            self._set_status(f"Perro '{name}' guardado correctamente.")
        else:
            messagebox.showerror("Pet Manager",
                                 "An error has occurred during the dog creation.\n\n"
                                 + self.ctlPet.getLastError("Dog"),
                                 parent=self)
            self._set_status("Error al guardar el perro.", error=True)

    def btnBuscarDogActionPerformed(self) -> None:
        """Busca un perro por su código."""
        code = self.txtCodeDog.get().strip()
        dog = self.ctlPet.SearchPet(code, "Dog")
        if dog is None:
            messagebox.showinfo("Pet Manager", "Code not found", parent=self)
            return

        self.txtPetId.set(str(dog.petId))
        self.txtDogId.set(str(dog.dogId))
        self.txtNameDog.set(dog.name)
        self.txtColorDog.set(dog.color)
        self.txtBornYearDog.set(str(dog.born_year))
        self.cbHealthStatusDog.set(dog.health_status)
        self.cbBreedDog.set(dog.breed)
        self.cbPedigree.set(bool(dog.pedigree))
        self._set_status(f"Perro '{dog.name}' encontrado.")

    def btnEditarDogActionPerformed(self) -> None:
        """Actualiza el perro buscado."""
        code = self.txtCodeDog.get().strip()
        name = self.txtNameDog.get().strip()
        color = self.txtColorDog.get().strip()

        try:
            born_year = int(self.txtBornYearDog.get().strip())
        except ValueError:
            messagebox.showinfo("Pet Manager", "You have to search the record to update",
                                 parent=self)
            return

        try:
            pet_id = int(self.txtPetId.get().strip())
            dog_id = int(self.txtDogId.get().strip())
        except ValueError:
            messagebox.showinfo("Pet Manager", "You have to search the record to update",
                                 parent=self)
            return

        dog = clsDog(dogId=dog_id, breed=self.cbBreedDog.get(),
                     pedigree=self.cbPedigree.get(), petId=pet_id, code=code,
                     name=name, born_year=born_year, color=color,
                     health_status=self.cbHealthStatusDog.get())

        if self.ctlPet.EditPet(dog):
            self.dogObjectList = self.ctlPet.ListPet("Dog")
            self.FillDogJlist()
            self.FillJlist()
            self.clearDogFields()
            self._refresh_all_reports()
            messagebox.showinfo("Pet Manager", "Record updated", parent=self)
            self._set_status(f"Perro '{name}' actualizado correctamente.")
        else:
            messagebox.showerror("Pet Manager", "Error updating the record\n\n"
                                 + self.ctlPet.getLastError("Dog"), parent=self)
            self._set_status("Error al actualizar el perro.", error=True)

    def btnEliminarDogActionPerformed(self) -> None:
        """Elimina el perro buscado."""
        pet_id = self.txtPetId.get().strip()
        dog_id = self.txtDogId.get().strip()

        if not pet_id or not dog_id:
            messagebox.showinfo("Pet Manager", "You have not searched a dog yet", parent=self)
            return

        try:
            dog = clsDog.fromIds(int(pet_id), int(dog_id))
        except ValueError:
            messagebox.showinfo(
                "Pet Manager",
                "Please, search a dog (by code) that you want to delete and try again...",
                parent=self)
            return

        if self.ctlPet.DeletePet(dog):
            self.dogObjectList = self.ctlPet.ListPet("Dog")
            self.FillDogJlist()
            self.FillJlist()
            self.clearDogFields()
            self._refresh_all_reports()
            messagebox.showinfo(
                "Pet Manager", "The dog has been deleted (removed) successfuly!", parent=self)
            self._set_status("Perro eliminado correctamente.")
        else:
            messagebox.showerror("Pet Manager",
                                 "An error has occurred during the dog deletion.\n\n"
                                 + self.ctlPet.getLastError("Dog"),
                                 parent=self)
            self._set_status("Error al eliminar el perro.", error=True)

    # ==================================================================
    # CRUD - GATOS
    # ==================================================================
    def btnCrearCatActionPerformed(self) -> None:
        """Guarda un gato nuevo."""
        code = self.txtCodeCat.get().strip()
        name = self.txtNameCat.get().strip()
        color = self.txtColorCat.get().strip()

        if not code or not name or not color:
            messagebox.showinfo("Pet Manager", "Fill all fields", parent=self)
            return

        try:
            born_year = int(self.txtBornYearCat.get().strip())
        except ValueError:
            messagebox.showinfo("Pet Manager", "Please add a valid born year", parent=self)
            return

        cat = clsCat(catId=0, breed=self.cbBreedCat.get(), petId=0, code=code,
                     name=name, born_year=born_year, color=color,
                     health_status=self.cbHealthStatusCat.get())

        if self.ctlPet.CreatePet(cat):
            self.catObjectList = self.ctlPet.ListPet("Cat")
            self.FillCatJlist()
            self.FillJlist()
            self.clearCatFields()
            self._refresh_all_reports()
            messagebox.showinfo("Pet Manager", "The record has been saved", parent=self)
            self._set_status(f"Gato '{name}' guardado correctamente.")
        else:
            messagebox.showerror("Pet Manager",
                                 "An error has occurred during the cat creation.\n\n"
                                 + self.ctlPet.getLastError("Cat"),
                                 parent=self)
            self._set_status("Error al guardar el gato.", error=True)

    def btnBuscarCatActionPerformed(self) -> None:
        """Busca un gato por su código."""
        code = self.txtCodeCat.get().strip()
        cat = self.ctlPet.SearchPet(code, "Cat")
        if cat is None:
            messagebox.showinfo("Pet Manager", "Code not found", parent=self)
            return

        self.txtPetId2.set(str(cat.petId))
        self.txtCatId.set(str(cat.catId))
        self.txtNameCat.set(cat.name)
        self.txtColorCat.set(cat.color)
        self.txtBornYearCat.set(str(cat.born_year))
        self.cbHealthStatusCat.set(cat.health_status)
        self.cbBreedCat.set(cat.breed)
        self._set_status(f"Gato '{cat.name}' encontrado.")

    def btnEditarCatActionPerformed(self) -> None:
        """Actualiza el gato buscado."""
        code = self.txtCodeCat.get().strip()
        name = self.txtNameCat.get().strip()
        color = self.txtColorCat.get().strip()

        try:
            born_year = int(self.txtBornYearCat.get().strip())
        except ValueError:
            messagebox.showinfo("Pet Manager", "You have to search the record to update",
                                 parent=self)
            return

        try:
            pet_id = int(self.txtPetId2.get().strip())
            cat_id = int(self.txtCatId.get().strip())
        except ValueError:
            messagebox.showinfo("Pet Manager", "You have to search the record to update",
                                 parent=self)
            return

        cat = clsCat(catId=cat_id, breed=self.cbBreedCat.get(), petId=pet_id, code=code,
                     name=name, born_year=born_year, color=color,
                     health_status=self.cbHealthStatusCat.get())

        if self.ctlPet.EditPet(cat):
            self.catObjectList = self.ctlPet.ListPet("Cat")
            self.FillCatJlist()
            self.FillJlist()
            self.clearCatFields()
            self._refresh_all_reports()
            messagebox.showinfo("Pet Manager", "Record updated", parent=self)
            self._set_status(f"Gato '{name}' actualizado correctamente.")
        else:
            messagebox.showerror("Pet Manager", "Error updating the record\n\n"
                                 + self.ctlPet.getLastError("Cat"), parent=self)
            self._set_status("Error al actualizar el gato.", error=True)

    def btnEliminarCatActionPerformed(self) -> None:
        """Elimina el gato buscado."""
        pet_id = self.txtPetId2.get().strip()
        cat_id = self.txtCatId.get().strip()

        if not pet_id or not cat_id:
            messagebox.showinfo("Pet Manager", "You have not searched a cat yet", parent=self)
            return

        try:
            cat = clsCat.fromIds(int(pet_id), int(cat_id))
        except ValueError:
            messagebox.showinfo(
                "Pet Manager",
                "Please, search a cat (by code) that you want to delete and try again...",
                parent=self)
            return

        if self.ctlPet.DeletePet(cat):
            self.catObjectList = self.ctlPet.ListPet("Cat")
            self.FillCatJlist()
            self.FillJlist()
            self.clearCatFields()
            self._refresh_all_reports()
            messagebox.showinfo(
                "Pet Manager", "The cat has been deleted (removed) successfuly!", parent=self)
            self._set_status("Gato eliminado correctamente.")
        else:
            messagebox.showerror("Pet Manager",
                                 "An error has occurred during the cat deletion.\n\n"
                                 + self.ctlPet.getLastError("Cat"),
                                 parent=self)
            self._set_status("Error al eliminar el gato.", error=True)

    # ==================================================================
    # EXPORTACIÓN A EXCEL
    # ==================================================================
    def btnExportarPetListActionPerformed(self) -> None:
        """Exporta perros + gatos a un archivo Excel."""
        try:
            self.dogObjectList = self.ctlPet.ListPet("Dog")
            self.catObjectList = self.ctlPet.ListPet("Cat")
            path = export_pet_list(self.dogObjectList, self.catObjectList)
            messagebox.showinfo("Pet Manager",
                                f"The file has been exported successfully:\n{path}",
                                parent=self)
            self._set_status(f"Reporte exportado en {path.name}")
        except Exception as exc:
            logger.error("Error al exportar la lista de mascotas: %s", exc)
            messagebox.showerror("Pet Manager", f"Error exporting the file:\n{exc}",
                                 parent=self)

    def btnExportarDogListActionPerformed(self) -> None:
        """Exporta la lista de perros a un archivo Excel."""
        try:
            self.dogObjectList = self.ctlPet.ListPet("Dog")
            path = export_dog_list(self.dogObjectList)
            messagebox.showinfo("Pet Manager",
                                f"The file has been exported successfully:\n{path}",
                                parent=self)
            self._set_status(f"Reporte exportado en {path.name}")
        except Exception as exc:
            logger.error("Error al exportar la lista de perros: %s", exc)
            messagebox.showerror("Pet Manager", f"Error exporting the file:\n{exc}",
                                 parent=self)

    def btnExportarCatListActionPerformed(self) -> None:
        """Exporta la lista de gatos a un archivo Excel."""
        try:
            self.catObjectList = self.ctlPet.ListPet("Cat")
            path = export_cat_list(self.catObjectList)
            messagebox.showinfo("Pet Manager",
                                f"The file has been exported successfully:\n{path}",
                                parent=self)
            self._set_status(f"Reporte exportado en {path.name}")
        except Exception as exc:
            logger.error("Error al exportar la lista de gatos: %s", exc)
            messagebox.showerror("Pet Manager", f"Error exporting the file:\n{exc}",
                                 parent=self)

    # ==================================================================
    # OTRAS ACCIONES
    # ==================================================================
    def btnRestartActionPerformed(self) -> None:
        """Reinicia la aplicación: recarga los datos y limpia los formularios.

        En Java se cerraba el formulario y se creaba uno nuevo; aquí se
        recarga todo el estado de la base de datos sin cerrar la ventana
        (equivalente funcional y más seguro dentro del depurador de VS Code).
        """
        try:
            self.clearDogFields()
            self.clearCatFields()
            self.load_data()
            self._set_status("Aplicación reiniciada: datos recargados desde la base de datos.")
            messagebox.showinfo("Pet Manager", "The application has been restarted", parent=self)
        except Exception as exc:
            logger.error("Error al reiniciar: %s", exc)
            messagebox.showerror("Pet Manager", f"Error restarting the application:\n{exc}",
                                 parent=self)

    def btnTestConnectionActionPerformed(self) -> None:
        """Comprueba la conexión con la base de datos MySQL."""
        ok, message = test_connection(self.db_data)
        if ok:
            messagebox.showinfo("Pet Manager", message, parent=self)
            self._set_status(message)
        else:
            messagebox.showerror("Pet Manager", message, parent=self)
            self._set_status("Sin conexión con la base de datos.", error=True)

    def btnRefreshReportsActionPerformed(self) -> None:
        """Recarga los tres gráficos y avisa al usuario."""
        self._refresh_all_reports()
        messagebox.showinfo("Pet Manager", "The report has been updated", parent=self)

    # ==================================================================
    # LIMPIEZA DE CAMPOS
    # ==================================================================
    def clearDogFields(self) -> None:
        """Limpia los campos del formulario de perro."""
        self.txtCodeDog.set("")
        self.txtNameDog.set("")
        self.txtColorDog.set("")
        self.txtBornYearDog.set("")
        self.txtPetId.set("")
        self.txtDogId.set("")
        self.cbBreedDog.set(DOG_BREEDS[0])
        self.cbHealthStatusDog.set(HEALTH_STATUS[0])
        self.cbPedigree.set(False)

    def clearCatFields(self) -> None:
        """Limpia los campos del formulario de gato."""
        self.txtCodeCat.set("")
        self.txtNameCat.set("")
        self.txtColorCat.set("")
        self.txtBornYearCat.set("")
        self.txtPetId2.set("")
        self.txtCatId.set("")
        self.cbBreedCat.set(CAT_BREEDS[0])
        self.cbHealthStatusCat.set(HEALTH_STATUS[0])


def main() -> None:
    """Punto de entrada de la ventana."""
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    app = frmPet()
    app.mainloop()


if __name__ == "__main__":
    main()
