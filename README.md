# 🐾 Pet Manager — Python + Tkinter + MySQL

Conversión completa del proyecto Java **Pet Manager** (NetBeans 8.2, Swing + JDBC + Apache POI + JFreeChart)
a **Python**, manteniendo la arquitectura **Modelo–Vista–Controlador (MVC)**:

| Capa | Java (antes) | Python (ahora) |
|------|--------------|----------------|
| Modelo | `Model/modelDog.java`, `Model/modelCat.java` | `Model/model_dog.py`, `Model/model_cat.py` |
| Conexión | `Model/DbData.java` + `mysql-connector-java` (`.jar`) | `Model/db_data.py` + `mysql-connector-python` (pip) |
| Controlador | `Controller/ctlPet.java` | `Controller/ctl_pet.py` |
| Vista | `View/frmPet.java` (Swing) | `View/frm_pet.py` (**Tkinter**) |
| Gráficos | JFreeChart | **matplotlib** (`View/charts.py`) |
| Exportar Excel | Apache POI (`.xls`) | **openpyxl** (`.xlsx`) (`View/excel_export.py`) |
| Entidades | `Classes/clsPet.java`, `clsDog`, `clsCat`, … | `Classes/cls_pet.py`, `cls_dog.py`, `cls_cat.py`, … |
| Interfaz Java | `Interfaces/IAnimal.java`, `IVertebrate.java` | `Interfaces/i_animal.py`, `i_vertebrate.py` |

La aplicación hace **CRUD completo** (Crear, Leer, Actualizar, Eliminar) contra la base de datos
MySQL **`gestormascotasbd`** que corre en tu servidor local **XAMPP / phpMyAdmin**.

### ⚡ Inicio rápido (ya está todo listo)

```powershell
cd C:\pet-manager-java-to-python\python
.venv\Scripts\Activate.ps1     # activa el entorno virtual
python main.py                  # abre la aplicación
```

| Script | Para qué sirve |
|--------|----------------|
| `python main.py` | Abre la aplicación (ventana Tkinter) |
| `python test_connection.py` | Comprueba la conexión con MySQL y lista las tablas |
| `python check_crud.py` | Ejecuta el CRUD completo y muestra el resultado de cada paso |
| `python check_app.py` | Verifica imports, gráficos, Excel y creación de la ventana |

> En Visual Studio Code: abre la carpeta **`python`** (no la raíz), y pulsa **F5**
> con la configuración *"Pet Manager (Tkinter)"*.

---

## 📑 Índice

1. [Requisitos previos](#1-requisitos-previos)
2. [Instalar Python (paso a paso)](#2-instalar-python-paso-a-paso)
3. [Estructura del proyecto](#3-estructura-del-proyecto)
4. [Paso a paso: base de datos en XAMPP / phpMyAdmin](#4-paso-a-paso-base-de-datos-en-xampp--phpmyadmin)
5. [Paso a paso: el "driver" (el equivalente del `.jar` de Java)](#5-paso-a-paso-el-driver-el-equivalente-del-jar-de-java)
6. [Paso a paso: preparar Visual Studio Code](#6-paso-a-paso-preparar-visual-studio-code)
7. [Paso a paso: probar la conexión](#7-paso-a-paso-probar-la-conexión)
8. [Paso a paso: ejecutar la aplicación](#8-paso-a-paso-ejecutar-la-aplicación)
9. [Estructura de la base de datos](#9-estructura-de-la-base-de-datos)
10. [Funciones de la interfaz](#10-funciones-de-la-interfaz)
11. [Solución de problemas (FAQ)](#11-solución-de-problemas-faq)
12. [Diferencias técnicas con el proyecto Java](#12-diferencias-técnicas-con-el-proyecto-java)
13. [Comandos útiles](#13-comandos-útiles)
14. [Estado de la verificación](#14-estado-de-la-verificación)

---

## 1. Requisitos previos

| Requisito | Detalle |
|-----------|---------|
| **Python 3.10 o superior** | ✅ **Ya instalado** (Python 3.12.10) — solo reinicia VS Code para que lo detecte |
| **XAMPP** | MySQL + Apache funcionando (panel de control → *Start* en MySQL) |
| **Visual Studio Code** | Con la extensión oficial **Python** (Microsoft) |
| **Entorno virtual `.venv`** | ✅ **Ya creado** con todas las dependencias instaladas |

> ⚠️ Antes de continuar, **cierra y vuelve a abrir Visual Studio Code**: el
> instalador de Python modificó el `PATH` y hasta que se reinicie la terminal
> el comando `python` seguirá apuntando al alias de Microsoft Store.

Comprobación rápida (en una terminal nueva):

```powershell
python --version     # -> Python 3.12.10
pip --version
```

---

## 2. Instalar Python (paso a paso)

> Python **ya está instalado** en este equipo. Si tuvieras que hacerlo de cero
> en otro PC, estos son los pasos (en este equipo el comando `python` apuntaba
> al **alias de Microsoft Store**, que no es Python real).

### 2.1 Instalar Python

**Opción A — desde la web (recomendada):**

1. Abre <https://www.python.org/downloads/windows/>
2. Pulsa el botón grande **"Download Python 3.x.x"**.
3. Ejecuta el instalador `.exe`.
4. ⚠️ **MUY IMPORTANTE:** en la primera pantalla marca la casilla
   **"Add python.exe to PATH"** (abajo a la izquierda) antes de pulsar *Install Now*.
5. Al terminar, cierra y reabre Visual Studio Code (para que recoja el PATH nuevo).

**Opción B — desde PowerShell (como administrador):**

```powershell
winget install --id Python.Python.3.12 -e
```

### 2.2 Desactivar el alias de Microsoft Store (si `python` no funciona)

1. Ve a **Configuración → Aplicaciones → Configuración avanzada de aplicaciones → Alias de ejecución de aplicaciones**
2. Apaga los interruptores de **python.exe** y **python3.exe**.
3. Cierra y reabre la terminal de VS Code.

> En este equipo **no hace falta**: el `PATH` real ya coloca
> `C:\Users\x360\AppData\Local\Programs\Python\Python312\` **antes** que
> `...\Microsoft\WindowsApps`, así que `python` y `py` funcionan correctamente
> en cualquier terminal nueva.

### 2.3 Comprobar que Python quedó instalado

```powershell
python --version
pip --version
```

Debe mostrar algo como `Python 3.12.x`. Si no funciona, reinicia la PC
o usa `py --version` (launcher de Python).

### 2.4 Comprobar que Tkinter está disponible

Tkinter viene incluido en Python (en Windows y macOS). Verifícalo con:

```powershell
python -c "import tkinter; print('Tkinter OK', tkinter.TkVersion)"
```

En Linux (si usas WSL/Ubuntu) habría que instalar `sudo apt install python3-tk`.

---

## 3. Estructura del proyecto

```
python/
│
├── Classes/                       # Entidades de dominio (como el paquete Java "Classes")
│   ├── __init__.py
│   ├── abst_hospital.py           #   AbstHospital (abstracta)
│   ├── cls_cat.py                 #   clsCat
│   ├── cls_doctor.py              #   clsDoctor
│   ├── cls_dog.py                 #   clsDog
│   ├── cls_pet.py                 #   clsPet (clase base)
│   ├── cls_report_by_health_status.py  # clsReportByHealthStatus
│   └── cls_veterinary.py          #   clsVeterinary
│
├── Interfaces/                    # Contratos (como el paquete Java "Interfaces")
│   ├── __init__.py
│   ├── i_animal.py                #   IAnimal
│   └── i_vertebrate.py            #   IVertebrate
│
├── Model/                         # Capa de datos (como el paquete Java "Model")
│   ├── __init__.py
│   ├── db_data.py                 #   DbData  (host, usuario, contraseña, base de datos)
│   ├── db_connection.py           #   apertura de conexión, cursores, transacciones
│   ├── model_cat.py               #   modelCat  (CRUD SQL de gatos)
│   └── model_dog.py               #   modelDog  (CRUD SQL de perros)
│
├── Controller/                    # Capa de control (como el paquete Java "Controller")
│   ├── __init__.py
│   └── ctl_pet.py                 #   ctlPet  (puente Vista <-> Modelo)
│
├── View/                          # Capa de presentación (como el paquete Java "View")
│   ├── __init__.py
│   ├── frm_pet.py                 #   frmPet  (ventana principal en Tkinter)
│   ├── charts.py                  #   gráficos con matplotlib (sustituye a JFreeChart)
│   └── excel_export.py            #   exporta a .xlsx con openpyxl (sustituye a Apache POI)
│
├── petmanager2/                   # Aplicación / punto de entrada
│   ├── __init__.py
│   └── pet_manager2.py            #   PetManager2 (equivalente a PetManager2.java)
│
├── .vscode/
│   ├── launch.json                # configuración de "Run and Debug" (F5)
│   └── settings.json              # intérprete virtual por defecto
│
├── main.py                        # ⭐ punto de entrada rápido:  python main.py
├── test_connection.py             # ⭐ script para probar la conexión con MySQL
├── check_crud.py                  # ⭐ suite que prueba el CRUD completo
├── check_app.py                   # ⭐ comprueba imports, gráficos, Excel y ventana
├── schema.sql                     # ⭐ creación de la base de datos y sus tablas
├── requirements.txt               # dependencias (pip)
├── .env.example                   # plantilla de configuración (cópiala como .env)
├── .gitignore
└── README.md                      # este archivo
```

---

## 4. Paso a paso: base de datos en XAMPP / phpMyAdmin

### 4.0 Estado actual de tu XAMPP (importante)

Al revisar tu servidor local se encontró lo siguiente:

| Base de datos | Estado | Contenido |
|---------------|--------|-----------|
| `administracionmascotasbd` | ✅ Ya existía (es la del proyecto Java) | 11 mascotas, 6 perros, 5 gatos + tablas `tb_doctor`, `tb_hospital`, `tb_pet_hospital` |
| `gestormascotasbd` | ✅ **Creada** al instalar este proyecto (importando `schema.sql`) | 3 mascotas de ejemplo + las mismas tablas |

Tienes **dos opciones**, ambas funcionan con el mismo código:

* **Opción A (la ya montada):** usar la base de datos nueva `gestormascotasbd`
  (es la que usa la aplicación por defecto).
* **Opción B (usar tus datos actuales):** cambiar `DB_NAME=administracionmascotasbd`
  en el archivo `.env` y listo.

> ⚠️ Detalle de la base antigua: en `administracionmascotasbd` la columna
> `code` es de **3 caracteres** (`varchar(3)`) y las claves primarias de
> `tb_dog` / `tb_cat` se llaman **`id`**. El programa detecta ambas cosas
> automáticamente, pero si usas códigos de más de 3 letras en esa base
> MySQL rechazará el INSERT (la interfaz te mostrará el error exacto).

### 4.1 Encender XAMPP

1. Abre **XAMPP Control Panel**.
2. Pulsa **Start** en **Apache** y en **MySQL** (deben ponerse en verde).
3. Comprueba que el puerto **3306** (MySQL) está activo.

### 4.2 Crear la base de datos `gestormascotasbd`

**Opción A — importando `schema.sql` (recomendado, hace todo de una vez):**

1. Abre <http://localhost/phpmyadmin>
2. Pestaña **Importar** (arriba).
3. **Choose File** → selecciona `C:\pet-manager-java-to-python\python\schema.sql`.
4. Deja marcada la base de datos o escribe `gestormascotasbd` en el campo de destino.
5. Pulsa **Continuar** / **Importar** (abajo a la derecha).

**Opción B — a mano:**

1. <http://localhost/phpmyadmin> → pestaña **SQL**.
2. Escribe (o pega) el siguiente SQL y pulsa **Ejecutar**:

```sql
CREATE DATABASE IF NOT EXISTS `gestormascotasbd`
    DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `gestormascotasbd`;
```

3. Después crea las tablas (mismo contenido que `schema.sql`, sección `CREATE TABLE`).

### 4.3 Comprobar el usuario y la contraseña de phpMyAdmin

Por defecto XAMPP usa **usuario `root` y contraseña vacía** — que es justo lo que
usa la aplicación por defecto (y es lo que se verificó al probar el proyecto).

Si tu instalación tiene otra contraseña:

- Opción 1: entra en <http://localhost/phpmyadmin> con esa contraseña y, en la
  pestaña **Cuentas de usuario**, cambia/establece la contraseña de `root`.
- Opción 2: define la contraseña en el archivo `.env` (ver sección 6.4).

### 4.4 (Opcional) Cambiar el puerto de MySQL

Si MySQL no está en el 3306 (por ejemplo, si tienes dos XAMPP o un MySQL de Oracle),
ajusta `DB_PORT` en el `.env`.

> Ojo: en este equipo hay **dos** instalaciones de XAMPP (`C:\xampp` y `D:\xampp`),
> pero la activa es `C:\xampp` (la de `D:\xampp` apunta al mismo `datadir`).
> Si MySQL no arranca, comprueba que estás usando `C:\xampp\mysql\bin\mysqld.exe`.

---

## 5. Paso a paso: el "driver" (el equivalente del `.jar` de Java)

### 5.1 La diferencia clave

| | Java | Python |
|---|------|--------|
| Driver | Archivo **`mysql-connector-java-8.x.jar`** que tenías que copiar **a mano** dentro de la carpeta `lib` de NetBeans | **Paquete de Python** instalado con `pip` (no hay que copiar ningún archivo a ninguna carpeta) |
| Cómo se carga | `Class.forName("com.mysql.jdbc.Driver")` | `import mysql.connector` |
| Dónde queda "instalado" | `NetBeans/platform/lib/` | En el **entorno virtual** del proyecto (`.venv`) |

En Python **no existe** el concepto de copiar un `.jar` a las librerías: el conector
se instala con `pip` dentro del entorno virtual y ya está disponible para el proyecto.

### 5.2 Eliges un driver (o los dos)

| Driver | Tipo | Comando | Notas |
|--------|------|---------|-------|
| `mysql-connector-python` | Oficial de Oracle/MySQL | `pip install mysql-connector-python` | **El mismo equipo** que mantiene el `mysql-connector-java`. Es el equivalente directo de tu `.jar`. |
| `pymysql` | 100 % Python (sin binario) | `pip install pymysql` | Alternativa ligera, útil si hay problemas con el binario oficial. |

El código de `Model/db_connection.py` **detecta automáticamente** cuál está instalado
y usa `mysql-connector-python` si ambos están presentes. Si no hay ninguno, muestra
un mensaje con el `pip install` exacto que falta.

### 5.3 Instalación en este proyecto

Desde la terminal de VS Code (con el entorno virtual activo, sección 6.3):

```powershell
pip install -r requirements.txt
```

o instala el driver suelto:

```powershell
pip install mysql-connector-python
```

### 5.4 Alternativa sin `pip`: usar el driver de Java

Si prefieres aprovechar el `.jar` que ya tienes, `PyMySQL` **no** lo necesita, pero
`mysql-connector-python` tampoco: es un módulo nativo de Python. No hay ningún
archivo `.jar` que copiar a ninguna carpeta.

---

## 6. Paso a paso: preparar Visual Studio Code

### 6.1 Abrir la carpeta correcta

En VS Code: **Archivo → Abrir carpeta…** y abre:

```
C:\pet-manager-java-to-python\python
```

> ⚠️ Abre **la carpeta `python`**, no la raíz `pet-manager-java-to-python`.
> Así los imports (`from Model…`, `from Classes…`) y la configuración de depuración funcionan.

### 6.2 Crear el entorno virtual (recomendado)

> ✅ **Ya está hecho**: la carpeta `.venv` existe en el proyecto con
> `mysql-connector-python`, `matplotlib` y `openpyxl` instalados.
> Los comandos que necesitarías en un PC nuevo son:

Abre la terminal integrada de VS Code (**Ctrl + `**) y ejecuta:

```powershell
python -m venv .venv
```

Actívalo:

```powershell
# PowerShell (Windows)
.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación por la política de ejecución:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

> En Linux/macOS sería `source .venv/bin/activate`.

VS Code detecta el entorno solo; si no, pulsa `Ctrl+Shift+P` →
**Python: Select Interpreter** → **`.venv\Scripts\python.exe`**.

*(La carpeta `.vscode/settings.json` ya apunta a ese intérprete por defecto.)*

### 6.3 Instalar las dependencias

Con el entorno virtual activo:

```powershell
pip install -r requirements.txt
```

Esto instala:

* `mysql-connector-python` → el driver MySQL (el sustituto del `.jar`)
* `matplotlib` → los gráficos de los reportes
* `openpyxl` → la exportación a Excel

Verifica lo instalado con:

```powershell
pip list
```

### 6.4 (Opcional) Archivo de configuración `.env`

Copia la plantilla y ajústala si tu XAMPP es diferente:

```powershell
Copy-Item .env.example .env
```

Contenido de `.env`:

```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=gestormascotasbd
DB_DRIVER=mysql-connector-python
```

Si **no** creas el `.env`, la aplicación usa exactamente esos mismos valores por defecto.
(El archivo `.env` está en `.gitignore` para que no subas tu contraseña a Git.)

### 6.5 Depuración con F5

El archivo `.vscode/launch.json` ya incluye dos configuraciones:

| Nombre | Qué ejecuta |
|--------|-------------|
| **Pet Manager (Tkinter)** | `main.py` → abre la ventana de la aplicación |
| **Probar conexión con MySQL** | `test_connection.py` → comprueba la base de datos |

Pulsa **F5** (o *Run and Debug* → elige la configuración → ▶).

---

## 7. Paso a paso: probar la conexión

Antes de abrir la GUI, comprueba que todo está bien. En la terminal de VS Code:

```powershell
python test_connection.py
```

Salida esperada:

```
======================================================================
 Pet Manager - prueba de conexión con MySQL
======================================================================
 Driver  : mysql-connector-python
 Host    : localhost
 Puerto  : 3306
 Usuario : root
 Base    : gestormascotasbd
 URL     : mysql://localhost:3306/gestormascotasbd
----------------------------------------------------------------------
 Conexión correcta a 'gestormascotasbd' (MySQL 8.0.35) en localhost:3306
----------------------------------------------------------------------
 Tablas en 'gestormascotasbd': tb_cat, tb_dog, tb_pet
   - tb_pet: 3 registro(s)
     columnas: id*, code, name, born_year, color, health_status
   - tb_dog: 2 registro(s)
     columnas: id_dog*, breed, pedigree, id_pet
   - tb_cat: 1 registro(s)
     columnas: id_cat*, breed, id_pet
======================================================================
 Todo correcto. Ya puede ejecutar la aplicación:  python main.py
======================================================================
```

El script **no abre ninguna ventana**: es ideal para depurar desde la terminal.

---

## 8. Paso a paso: ejecutar la aplicación

### 8.1 Desde la terminal

```powershell
python main.py
```

### 8.2 Desde Visual Studio Code

* Botón **▶ Run Python File** arriba a la derecha del editor, o
* **F5** con la configuración *"Pet Manager (Tkinter)"*.

### 8.3 Alternativas

```powershell
# Como módulo (desde la carpeta python)
python -m petmanager2.pet_manager2
```

### 8.4 Si la ventana no aparece

* En algunos sistemas, la app debe ejecutarse **desde la terminal integrada**
  (no desde la consola de depuración) para que Tkinter pueda crear la ventana.
* Comprueba que `tkinter` está instalado: `python -m tkinter` debe abrir una
  ventana de prueba.

---

## 9. Estructura de la base de datos

```
gestormascotasbd
├── tb_pet          (id*, code, name, born_year, color, health_status)   ← datos generales
├── tb_dog          (id*, breed, pedigree, id_pet → tb_pet.id)           ← datos del perro
├── tb_cat          (id*, breed, id_pet → tb_pet.id)                     ← datos del gato
├── tb_doctor       (id*, name, phone, address)                         ← módulo veterinario
├── tb_hospital     (id*, name, phone, address, patien_type, id_doctor)  ← módulo veterinario
└── tb_pet_hospital (id*, id_pet, id_hospital)                           ← historial de atendencias
```

`*` = clave primaria. `id_pet` es la clave foránea que une cada perro/gato con su
mascota en `tb_pet` (relación 1 a 1). **Las tablas NO tienen `ON DELETE CASCADE`**
a propósito: por eso el borrado elimina primero el registro específico
(`tb_dog` / `tb_cat`) y después el general (`tb_pet`), tal como explicaba el
comentario del código Java original.

Los datos de salud posibles son: `Sick`, `Healthy`, `In Surgery`.

> **Sobre el proyecto Java original:** allí el `DELETE` usaba `tb_cat.id`
> mientras que el `UPDATE` usaba `tb_cat.id_cat` (nombres inconsistentes, lo que
> rompía la edición). En esta versión el nombre real de la clave primaria se
> **resuelve en tiempo de ejecución** leyendo `INFORMATION_SCHEMA`, así que
> funciona tanto con `id_cat`/`id_dog` como con `id` sin tocar el código
> (es lo que hace con tu base `administracionmascotasbd`, que usa `id`).

---

## 10. Funciones de la interfaz

Ventana **"Pet Manager"** con 8 pestañas y una barra de estado inferior:

| Pestaña | Contenido |
|---------|-----------|
| **Pet List** | Todas las mascotas (perros + gatos): código, nombre y tipo |
| **Dog Manager** | Formulario del perro: Code, Name, Born year, Color, Health Status, Breed, Pedigree, petId, dogId + botones **Save / Search / Edit / Delete** |
| **Cat Manager** | Formulario del gato: Code, Name, Born year, Color, Health Status, Breed, petId, catId + botones **Save / Search / Edit / Delete** |
| **Dog List** | Solo los perros |
| **Cat List** | Solo los gatos |
| **Report By Health Status** | Gráfico circular (pie 3D) con el total de mascotas por estado de salud |
| **Dog Report** | Gráfico de barras vertical con los perros por estado de salud |
| **Cat Report** | Gráfico de barras horizontal con los gatos por estado de salud |

Botones de la cabecera:

| Botón | Acción |
|-------|--------|
| **Export Pet List** | Exporta perros + gatos a `reportes/pet_list_report_date_AAAAMMDD_HH-MM-SS.xlsx` |
| **Export Dog List** | Exporta solo perros a `reportes/dog_list_report_date_....xlsx` |
| **Export Cat List** | Exporta solo gatos a `reportes/cat_list_report_date_....xlsx` |
| **Restart** | Recarga los datos de la BD y limpia los formularios |
| **Test connection** | Comprueba la conexión con MySQL y muestra el resultado |

---

## 11. Solución de problemas (FAQ)

### ❌ `python` abre la Microsoft Store / "no se encontró Python"

Es el *alias* de ejecución de Windows, no Python real.

1. Instala Python desde <https://www.python.org/downloads/windows/> marcando
   **"Add python.exe to PATH"**.
2. Desactiva los alias en *Configuración → Apps → Configuración avanzada de aplicaciones →
   Alias de ejecución de aplicaciones*.

### ❌ `ModuleNotFoundError: No module named 'mysql'`

El driver no está instalado en el intérprete que estás usando.

```powershell
pip install -r requirements.txt
# o solo el driver:
pip install mysql-connector-python
```

Comprueba que estás usando el intérprete correcto:
`Ctrl+Shift+P` → **Python: Select Interpreter** → `.venv\Scripts\python.exe`.
Desde la terminal puedes ver cuál se usa con `where python` y `pip -V`.

### ❌ `Access denied for user 'root'@'localhost'`

La contraseña no coincide.

* Comprueba la contraseña en <http://localhost/phpmyadmin>.
* Si tu XAMPP tiene contraseña, ponla en `.env` (`DB_PASSWORD=...`).
* Alternativa: en phpMyAdmin → pestaña **Cuentas de usuario** → `root` →
  *Editar* → deja la contraseña vacía o cámbiala y actualiza el `.env`.

### ❌ `Unknown database 'gestormascotasbd'`

La base de datos no existe. Créala (sección 4.2) importando `schema.sql`.

### ❌ `Can't connect to MySQL server on 'localhost' (10061)`

MySQL de XAMPP no está arrancado. En el **XAMPP Control Panel** pulsa *Start* en MySQL.
Comprueba también el puerto (por defecto 3306) y que no haya otro servicio
usándolo (por ejemplo, un MySQL de Oracle instalado en el PC).

### ❌ `Access denied for user 'root'@'localhost' (using password: YES)` con MySQL 8

MySQL 8 usa `caching_sha2_password`. Los conectores modernos lo soportan; si te
ocurre, en phpMyAdmin ejecuta:

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';
FLUSH PRIVILEGES;
```

y luego reinicia MySQL en XAMPP.

### ❌ `The server time zone value '...' is unrecognized`

Añade el parámetro de zona horaria al final de la URL de conexión
(`Model/db_data.py`, método `jdbc_url` → no es el que se usa) o exporta la variable:

```powershell
$env:TZ = "UTC"
```

Alternativamente, en `Model/db_connection.py` añade `time_zone="+00:00"` a la llamada
`mysql.connector.connect(...)`.

### ❌ La ventana no sale / se cierra al instante

* Ejecuta desde la **terminal integrada** de VS Code, no desde la consola de depuración.
* Comprueba `python -m tkinter` (debe abrir una ventana de prueba).
* Revisa el log en la terminal: los errores de MySQL se muestran en la barra de estado
  y en el log (`logging` escribe en la consola).

### ❌ `No module named 'matplotlib'` / `'openpyxl'`

```powershell
pip install -r requirements.txt
```

### ❌ ¿Y si quiero usar la base de datos que ya tengo (otra nombre)?

Edita `DB_NAME` en el `.env` o el valor `DEFAULT_DATABASE` de `Model/db_data.py`.
El proyecto Java usaba `administracionmascotasbd`; esta versión usa
`gestormascotasbd` por defecto.

---

## 12. Diferencias técnicas con el proyecto Java

Además del cambio de Swing→Tkinter y JDBC→`mysql-connector-python`, esta versión
corrige y mejora algunos puntos del código original:

| Aspecto | Java original | Python actual |
|---------|---------------|---------------|
| Lectura de filas | `result.getInt(1)`, `getString(2)`… (posicional, frágil) | Diccionario por nombre de columna (`fila["code"]`) |
| `SELECT` | `SELECT *` | Columnas explícitas |
| Clave primaria | Nombre fijo e inconsistente (`id` vs `id_cat`) | Se resuelve en tiempo de ejecución con `INFORMATION_SCHEMA` |
| Transacciones | `commit()` entre los dos `DELETE` (anulaba el *savepoint*) | Un único `commit` con `SAVEPOINT`/`ROLLBACK TO SAVEPOINT` → borrado atómico |
| **Resultado del CRUD** | `ctlPet` devolvía **siempre `true`** (ignoraba el resultado del modelo) → la GUI decía "Record updated" aunque no se hubiera guardado nada | El controlador devuelve el **resultado real** del modelo y la GUI muestra el error de MySQL concreto |
| `rowcount` en UPDATE | Filas *cambiadas* (guardar sin cambios = 0 = "error") | Conexión con `FOUND_ROWS` → filas *encontradas* (guardar sin cambios no es un error) |
| Errores | `catch (Exception e) { return false; }` (sin detalle) | Se registran en el log (`logging`) y se muestran en el diálogo de error |
| Exportar Excel | `.xls` con Apache POI | `.xlsx` con openpyxl (formato moderno) |
| Gráficos | JFreeChart (3 paneles con `ChartPanel`) | matplotlib embebido con `FigureCanvasTkAgg` + barra de herramientas |
| Diálogos | `JOptionPane` | `tkinter.messagebox` (`showinfo` / `showerror`) |
| Botón *Restart* | Cerraba y recreaba el `JFrame` | Recarga los datos y limpia los formularios (equivalente y más seguro en el depurador) |
| Acceso a datos | `getX()` / `setX()` | *Properties* de Python (`pet.code`), manteniendo `getAnimalType()` / `getNumberOfBones()` por compatibilidad con las interfaces |
| Listas | `JList` con texto `"nombre - código - tipo"` | `ttk.Treeview` con columnas Code / Name / Type (misma información, mejor presentación) |

---

## 13. Comandos útiles

```powershell
# Activar el entorno virtual
.venv\Scripts\Activate.ps1

# Instalar dependencias (solo si las cambias)
pip install -r requirements.txt

# Instalar / actualizar un paquete concreto
pip install --upgrade mysql-connector-python

# Ver qué hay instalado
pip list

# Probar la conexión con la base de datos
python test_connection.py

# Ejecutar la aplicación
python main.py

# Ejecutar la aplicación como módulo
python -m petmanager2.pet_manager2

# Suite de comprobaciones (CRUD completo contra la base de datos)
python check_crud.py

# Comprobación de que todo importa y la ventana se construye bien
python check_app.py

# Ver los logs con más detalle
$env:PYTHONVERBOSE = "1"; python main.py
```

### Scripts de comprobación incluidos

| Script | Qué hace |
|--------|----------|
| `test_connection.py` | Comprueba la conexión, lista las tablas, sus columnas y el número de filas |
| `check_crud.py` | Ejecuta el CRUD completo (crear, buscar, listar, actualizar, borrar, reportes) y muestra el resultado de cada paso |
| `check_app.py` | Importa todos los módulos, genera los 3 gráficos, exporta un Excel y crea la ventana (no abre el bucle de eventos) |

---

## 14. Estado de la verificación

Todo lo anterior se ejecutó y se probó en este equipo:

| Prueba | Resultado |
|--------|-----------|
| Compilación de los 30 archivos `.py` | ✅ Sin errores de sintaxis |
| Importación de todos los módulos | ✅ OK |
| Creación de la ventana con sus 8 pestañas | ✅ OK |
| Gráficos (circular + 2 de barras) | ✅ OK |
| Exportación a Excel (`.xlsx` real) | ✅ OK |
| Conexión con MySQL (`localhost:3306`, `root`) | ✅ OK |
| CRUD completo contra `gestormascotasbd` | ✅ **Todas las pruebas pasaron** |
| Compatibilidad con `administracionmascotasbd` (la base de datos que ya tenías) | ✅ OK (lectura, búsqueda y reportes) |

---

¡Listo! Si la conexión funciona en `test_connection.py`, la aplicación GUI
funcionará exactamente igual. 🎉
