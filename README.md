# API REST Sakila – FastAPI + MariaDB

Este proyecto es una API REST desarrollada con **FastAPI** y **MariaDB/MySQL** utilizando la base de datos de ejemplo **Sakila**.  
Forma parte de la asignatura de **Acceso a Datos (AAD)** y tiene como objetivo practicar:

- Conexión a base de datos relacional desde Python
- Uso de *pools* de conexiones
- Desarrollo de una API REST sin ORM (solo SQL)
- Organización del código en módulos (customers, rentals)
- Documentación automática con Swagger (/docs)

---

## 1. Tecnologías utilizadas

- **Lenguaje:** Python 3.x
- **Framework API:** FastAPI
- **Servidor ASGI:** Uvicorn
- **Base de datos:** MariaDB / MySQL
- **Driver:** mysql-connector-python
- **Gestión de configuración:** python-dotenv
- **Validación de emails:** email-validator

---

## 2. Estructura del proyecto

```text
API/
│
├── app/
│   ├── __init__.py          # Marca la carpeta como paquete Python
│   ├── main.py              # Punto de entrada de FastAPI
│   ├── db.py                # Conexión y pool de conexiones a la BD
│   ├── schemas.py           # Modelos Pydantic (customers, rentals)
│   ├── customers.py         # Endpoints relacionados con clientes
│   └── rentals.py           # Endpoints relacionados con alquileres
│
├── venv/                    # Entorno virtual (no se sube al repo)
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Este documento


---

## INTRUCCIONES PARA INSTALAR Y EJECUTAR LA API

1. Clonar mi repositorio

git clone https://github.com/lluis22-mas/Proyecto-ADD-API.git
cd Proyecto-ADD-API

2. Crear entorno virtual

Windows

python -m venv venv
venv\Scripts\activate

3. Instalar dependencias

pip install -r requirements.txt

4. Configurar la base de datos 

La API utiliza la bas de datos Sakila (MySQL/MariaDB)

5. Crear archivo .env

DB_HOST=localhost
DB_PORT=3305
DB_USER=root
DB_PASSWORD=1234
DB_NAME=sakila

6. Ejecutar la API

Con el entorno virtual activado:

uvicorn app.main:app --reload

La API estará disponible en:

http://127.0.0.1:8000

La documentación interactiva (Swagger UI):

http://127.0.0.1:8000/docs

7. Endopints principales 

Customers

POST /api/v1/customers → crear cliente

GET /api/v1/customers → listar clientes

GET /api/v1/customers/{id} → obtener cliente

PUT /api/v1/customers/{id} → actualizar cliente

DELETE /api/v1/customers/{id} → eliminar cliente

Rentals

POST /api/v1/rentals → crear alquiler

GET /api/v1/rentals → listar alquileres

GET /api/v1/rentals/{id} → obtener alquiler

PUT /api/v1/rentals/{id}/return → marcar alquiler como devuelto

GET /api/v1/rentals/customer/{id} → alquileres de un cliente

8. Notas importantes

- Cada endpoint abre y cierra conexiones a la BD manualmente sin usar ORM
- Se usa un pool de conexiones para mayor eficiencia.
-La carpeta app/ contiene los módulos principales:

db.py → conexión

schemas.py → modelos

customers.py → CRUD de clientes

rentals.py → CRUD de alquileres

main.py → registro de routers y punto de entrada
- El servidor se reinicia automáticamente al modificar código (--reload).