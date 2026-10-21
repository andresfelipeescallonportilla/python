"""Prueba de humo: importa todos los modulos, crea la GUI y la destruye."""
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

print("== 1. Importaciones ==")
try:
    from Classes.cls_pet import clsPet
    from Classes.cls_dog import clsDog
    from Classes.cls_cat import clsCat
    from Classes.cls_doctor import clsDoctor
    from Classes.cls_veterinary import clsVeterinary
    from Classes.cls_report_by_health_status import clsReportByHealthStatus
    from Classes.abst_hospital import AbstHospital
    from Interfaces.i_animal import IAnimal
    from Interfaces.i_vertebrate import IVertebrate
    from Model.db_data import DbData
    from Model.db_connection import test_connection
    from Model.model_dog import modelDog
    from Model.model_cat import modelCat
    from Controller.ctl_pet import ctlPet
    from View.frm_pet import frmPet
    from View.charts import build_pie_figure, build_bar_figure
    from View.excel_export import export_pet_list
    print("   OK - todos los modulos importan")

    print("== 2. Modelo de dominio ==")
    dog = clsDog(dogId=1, breed="Pincher", pedigree=True, petId=10, code="P01",
                 name="Firulais", born_year=2018, color="Marron", health_status="Healthy")
    cat = clsCat(catId=2, breed="British", petId=11, code="P02", name="Michi",
                 born_year=2020, color="Negro", health_status="Sick")
    print("   dog ->", dog.getAnimalType(), dog.getNumberOfBones(), dog.code, dog.pedigree)
    print("   cat ->", cat.getAnimalType(), cat.getNumberOfBones(), cat.code)
    assert isinstance(dog, clsPet) and isinstance(dog, IAnimal) and isinstance(dog, IVertebrate)
    d2 = clsDog.fromIds(10, 1)
    assert d2.petId == 10 and d2.dogId == 1
    vet = clsVeterinary("Clínica", "555", "Calle 1", clsDoctor("Dr", "LIC-1"))
    print("   vet ->", vet.getPatientType(), vet.Surgery(), vet.getHospitalInformation())
    rep = clsReportByHealthStatus("Healthy", 3)
    print("   report ->", rep.health_status, rep.amount_of_pets_by_health_status)

    print("== 3. Graficos (matplotlib) ==")
    fig1 = build_pie_figure([rep])
    fig2 = build_bar_figure([rep], "Perros", "Estado", "Cantidad", "vertical")
    fig3 = build_bar_figure([rep], "Gatos", "Estado", "Cantidad", "horizontal")
    print("   OK - 3 figuras creadas")

    print("== 4. Exportacion a Excel (openpyxl) ==")
    path = export_pet_list([dog], [cat], output_dir=ROOT / "reportes")
    print("   OK ->", path.name, f"({path.stat().st_size} bytes)")

    print("== 5. Configuracion de la BD ==")
    db = DbData()
    print("   ", db)

    print("== 6. Conexion con MySQL ==")
    ok, msg = test_connection(db)
    print("   ", "OK" if ok else "SIN CONEXION", "->", msg.splitlines()[0])

    print("== 7. Creacion de la ventana Tkinter ==")
    app = frmPet(db)
    app.update_idletasks()
    app.update()
    print("   OK - ventana creada, pestanas:",
          [app.notebook.tab(tab, "text") for tab in app.notebook.tabs()])
    print("   OK - estado:", app.lbl_status.cget("text") or "(vacio)")
    app.destroy()
    print("== SMOKE TEST OK ==")
except Exception:
    traceback.print_exc()
    sys.exit(1)
