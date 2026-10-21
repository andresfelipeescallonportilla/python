"""Utilidad de línea de comandos para comprobar la conexión con MySQL.

Uso::

    python test_connection.py

Muestra:

* la configuración de conexión que se está usando;
* si la conexión con la base de datos ``gestormascotasbd`` funciona;
* las tablas que existen y el número de registros de cada una.

Es el paso previo recomendado antes de abrir la GUI (ver ``README.md``).
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Model.db_connection import connection, cursor, test_connection  # noqa: E402
from Model.db_data import DbData  # noqa: E402

TABLES = ("tb_pet", "tb_dog", "tb_cat")


def main() -> int:
    db_data = DbData()

    print("=" * 70)
    print(" Pet Manager - prueba de conexión con MySQL")
    print("=" * 70)
    print(f" Driver  : {db_data.driver}")
    print(f" Host    : {db_data.host}")
    print(f" Puerto  : {db_data.port}")
    print(f" Usuario : {db_data.user}")
    print(f" Base    : {db_data.database}")
    print(f" URL     : {db_data.url}")
    print("-" * 70)

    ok, message = test_connection(db_data)
    print(f" {message}")
    if not ok:
        print("\n Revisa: XAMPP iniciado (MySQL + Apache), usuario/contraseña de")
        print(" phpMyAdmin y que la base de datos exista en la pestaña 'Importar'.")
        return 1

    print("-" * 70)
    try:
        with connection(db_data) as conn:
            with cursor(conn) as cur:
                cur.execute(
                    "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES "
                    "WHERE TABLE_SCHEMA = DATABASE() ORDER BY TABLE_NAME"
                )
                existing = [row["TABLE_NAME"] for row in cur.fetchall()]
                print(f" Tablas en '{db_data.database}': {', '.join(existing) or '(ninguna)'}")

                for table in TABLES:
                    if table not in existing:
                        print(f"   - {table}: NO EXISTE (importa schema.sql)")
                        continue
                    cur.execute(f"SELECT COUNT(*) AS total FROM `{table}`")
                    total = cur.fetchone()["total"]
                    print(f"   - {table}: {total} registro(s)")

                    cur.execute(
                        "SELECT COLUMN_NAME, COLUMN_KEY FROM INFORMATION_SCHEMA.COLUMNS "
                        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s "
                        "ORDER BY ORDINAL_POSITION",
                        (table,),
                    )
                    columns = ", ".join(
                        f"{row['COLUMN_NAME']}"
                        f"{'*' if row['COLUMN_KEY'] == 'PRI' else ''}"
                        for row in cur.fetchall()
                    )
                    print(f"     columnas: {columns}")
    except Exception as exc:  # pragma: no cover
        print(f" Error consultando la base de datos: {exc}")
        return 1

    print("=" * 70)
    print(" Todo correcto. Ya puede ejecutar la aplicación:  python main.py")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
