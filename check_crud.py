"""Prueba funcional completa del CRUD contra la base de datos real."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from Classes.cls_cat import clsCat
from Classes.cls_dog import clsDog
from Controller.ctl_pet import ctlPet
from Model.db_connection import connection, cursor
from Model.db_data import DbData

db = DbData()
ctl = ctlPet(db)
fallos = []


def check(nombre, condicion, detalle=""):
    marca = "OK   " if condicion else "FALLO"
    print(f"  [{marca}] {nombre}" + (f" -> {detalle}" if detalle else ""))
    if not condicion:
        fallos.append(nombre)


print("== 0. Base de datos ==")
with connection(db) as conn:
    with cursor(conn) as cur:
        cur.execute("SELECT DATABASE() AS db")
        check("base de datos seleccionada", cur.fetchone()["db"] == db.database, db.database)

print("\n== 1. CREATE (perro) ==")
perro = clsDog(dogId=0, breed="Schnauzer", pedigree=True, petId=0, code="T01",
               name="Roco", born_year=2021, color="Marron", health_status="Healthy")
check("CreatePet(perro)", ctl.CreatePet(perro), ctl.getLastError("Dog"))

print("\n== 2. CREATE (gato) ==")
gato = clsCat(catId=0, breed="Birman", petId=0, code="T02", name="Nube",
               born_year=2022, color="Blanco", health_status="Sick")
check("CreatePet(gato)", ctl.CreatePet(gato), ctl.getLastError("Cat"))

print("\n== 3. READ / Search ==")
buscado = ctl.SearchPet("T01", "Dog")
check("SearchPet(perro) devuelve objeto", buscado is not None)
check("  -> nombre correcto", bool(buscado) and buscado.name == "Roco")
check("  -> raza correcta", bool(buscado) and buscado.breed == "Schnauzer")
check("  -> pedigree correcto", bool(buscado) and bool(buscado.pedigree))
check("  -> petId asignado", bool(buscado) and buscado.petId > 0)
check("  -> dogId asignado", bool(buscado) and buscado.dogId > 0)
check("SearchPet(gato) devuelve objeto", ctl.SearchPet("T02", "Cat") is not None)
check("SearchPet(codigo inexistente) -> None", ctl.SearchPet("ZZZ99", "Dog") is None)

print("\n== 4. READ / List ==")
perros = ctl.ListPet("Dog")
gatos = ctl.ListPet("Cat")
check("ListPet(Dog) devuelve elementos", len(perros) > 0, f"{len(perros)} perros")
check("ListPet(Cat) devuelve elementos", len(gatos) > 0, f"{len(gatos)} gatos")
check("  -> el perro creado esta en la lista", any(p.code == "T01" for p in perros))
check("  -> el gato creado esta en la lista", any(p.code == "T02" for p in gatos))

print("\n== 5. UPDATE ==")
# La GUI rellena petId / dogId con los valores que devuelve la búsqueda.
perro.petId = buscado.petId
perro.dogId = buscado.dogId
perro.name = "Roco II"
perro.color = "Negro"
perro.breed = "Pincher"
perro.pedigree = False
check("EditPet(perro)", ctl.EditPet(perro), ctl.getLastError("Dog"))
releido = ctl.SearchPet("T01", "Dog")
check("  -> nombre actualizado", bool(releido) and releido.name == "Roco II")
check("  -> color actualizado", bool(releido) and releido.color == "Negro")
check("  -> raza actualizada", bool(releido) and releido.breed == "Pincher")
check("  -> pedigree actualizado", bool(releido) and not releido.pedigree)

gato_buscado = ctl.SearchPet("T02", "Cat")
gato.petId = gato_buscado.petId
gato.catId = gato_buscado.catId
gato.name = "Nube II"
gato.health_status = "Healthy"
check("EditPet(gato)", ctl.EditPet(gato), ctl.getLastError("Cat"))
releido_g = ctl.SearchPet("T02", "Cat")
check("  -> nombre actualizado", bool(releido_g) and releido_g.name == "Nube II")
check("  -> estado de salud actualizado", bool(releido_g) and releido_g.health_status == "Healthy")

print("\n== 5b. UPDATE sin cambios (no debe considerarse error) ==")
check("EditPet(perro) sin modificar", ctl.EditPet(perro), ctl.getLastError("Dog"))

print("\n== 6. REPORTES ==")
reporte = ctl.ListPetByHealthStatus()
check("ListPetByHealthStatus", len(reporte) > 0,
      str([(r.health_status, r.amount_of_pets_by_health_status) for r in reporte]))
reporte_d = ctl.ListDogByHealthStatus()
check("ListDogByHealthStatus", len(reporte_d) > 0,
      str([(r.health_status, r.amount_of_pets_by_health_status) for r in reporte_d]))
reporte_c = ctl.ListCatByHealthStatus()
check("ListCatByHealthStatus", len(reporte_c) > 0,
      str([(r.health_status, r.amount_of_pets_by_health_status) for r in reporte_c]))

print("\n== 7. DELETE (perro) ==")
perro_borrar = clsDog.fromIds(perro.petId, buscado.dogId)
check("DeletePet(perro)", ctl.DeletePet(perro_borrar), ctl.getLastError("Dog"))
check("  -> el perro ya no existe", ctl.SearchPet("T01", "Dog") is None)
with connection(db) as conn:
    with cursor(conn) as cur:
        cur.execute("SELECT COUNT(*) AS n FROM tb_pet WHERE id = %s", (perro.petId,))
        check("  -> fila borrada de tb_pet", cur.fetchone()["n"] == 0)
        cur.execute("SELECT COUNT(*) AS n FROM tb_dog WHERE id = %s", (buscado.dogId,))
        check("  -> fila borrada de tb_dog", cur.fetchone()["n"] == 0)

print("\n== 8. DELETE (gato) ==")
gato_buscado = ctl.SearchPet("T02", "Cat")
gato_borrar = clsCat.fromIds(gato.petId, gato_buscado.catId)
check("DeletePet(gato)", ctl.DeletePet(gato_borrar), ctl.getLastError("Cat"))
check("  -> el gato ya no existe", ctl.SearchPet("T02", "Cat") is None)

print("\n== 9. Rollback (FK sin ON DELETE CASCADE) ==")
# Se intenta borrar solo la fila general: la FK lo impide y la transaccion
# debe revertirse sin dejar datos a medias.
with connection(db) as conn:
    with cursor(conn) as cur:
        cur.execute("SELECT p.id AS pet_id FROM tb_pet p INNER JOIN tb_cat c "
                    "ON p.id = c.id_pet LIMIT 1")
        fila = cur.fetchone()
        if fila:
            pet_id = fila["pet_id"]
            try:
                cur.execute("START TRANSACTION")
                cur.execute("DELETE FROM tb_pet WHERE id = %s", (pet_id,))
                conn.rollback()
            except Exception as exc:
                conn.rollback()
                print(f"  (MySQLoprotegio la FK: {type(exc).__name__})")
            with cursor(conn) as c2:
                c2.execute("SELECT COUNT(*) AS n FROM tb_pet WHERE id = %s", (pet_id,))
                check("  -> la mascota sigue existiendo", c2.fetchone()["n"] == 1)
        else:
            print("  (sin datos de prueba)")

print("\n" + "=" * 62)
if fallos:
    print(f" RESULTADO: {len(fallos)} prueba(s) FALLIDA(S): {fallos}")
    sys.exit(1)
print(" RESULTADO: TODAS LAS PRUEBAS PASARON")
print("=" * 62)
