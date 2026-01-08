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

Request:

{
  "first_name": "LLUIS",
  "last_name": "TEST",
  "email": "lluis.test@example.com",
  "address_id": 5,
  "store_id": 1,
  "active": 1
}

Respuesta esperada (201 Created):

{
  "customer_id": 605,
  "first_name": "LLUIS",
  "last_name": "TEST",
  "email": "lluis.test@example.com",
  "address_id": 5,
  "store_id": 1,
  "active": 1,
  "create_date": "2025-01-10T10:15:30",
  "last_update": "2025-01-10T10:15:30"
}


GET /api/v1/customers → listar clientes

Parámetros opcionales:

- limit (por defecto 100)
- offset (por defecto 0)

Respuesta esperada (200 OK):

[
  {
    "customer_id": 1,
    "first_name": "MARY",
    "last_name": "SMITH",
    "email": "mary.smith@example.com",
    "address_id": 5,
    "store_id": 1,
    "active": 1,
    "create_date": "2006-02-14T22:04:36",
    "last_update": "2006-02-15T04:57:12"
  }
]

GET /api/v1/customers/{id} → obtener cliente

Respuesta esperada (200 OK):

{
  "customer_id": 1,
  "first_name": "MARY",
  "last_name": "SMITH",
  "email": "mary.smith@example.com",
  "address_id": 5,
  "store_id": 1,
  "active": 1,
  "create_date": "2006-02-14T22:04:36",
  "last_update": "2006-02-15T04:57:12"
}

Error si no existe (404):

{
  "detail": "Customer not found"
}


PUT /api/v1/customers/{id} → actualizar cliente

Request:

{
  "first_name": "LLUIS",
  "last_name": "ACTUALIZADO",
  "email": "lluis.new@example.com",
  "address_id": 6,
  "store_id": 1,
  "active": 1
}

Respuesta esperada (200 OK):

{
  "customer_id": 605,
  "first_name": "LLUIS",
  "last_name": "ACTUALIZADO",
  "email": "lluis.new@example.com",
  "address_id": 6,
  "store_id": 1,
  "active": 1,
  "create_date": "2025-01-10T10:15:30",
  "last_update": "2025-01-10T10:30:00"
}

DELETE /api/v1/customers/{id} → eliminar cliente

Respuesta esperada:

- 204 No Content

Error si no existe (404):

{
  "detail": "Customer not found"
}


Rentals

POST /api/v1/rentals → crear alquiler

Request:

{
  "inventory_id": 1,
  "customer_id": 1,
  "staff_id": 1
}

Respuesta esperada (201 Created):

{
  "rental_id": 16050,
  "inventory_id": 1,
  "customer_id": 1,
  "staff_id": 1,
  "rental_date": "2025-01-10T11:00:00",
  "return_date": null,
  "last_update": "2025-01-10T11:00:00"
}

Error si el inventario ya está alquilado (400):

{
  "detail": "Inventory is already rented (open rental exists)"
}


GET /api/v1/rentals → listar alquileres

Respuesta esperada (200 OK):

[
  {
    "rental_id": 16050,
    "inventory_id": 1,
    "customer_id": 1,
    "staff_id": 1,
    "rental_date": "2025-01-10T11:00:00",
    "return_date": "2025-01-12T10:00:00",
    "last_update": "2025-01-12T10:00:00"
  }
]


GET /api/v1/rentals/{id} → obtener alquiler

Respuesta esperada (200 OK):

{
  "rental_id": 16050,
  "inventory_id": 1,
  "customer_id": 1,
  "staff_id": 1,
  "rental_date": "2025-01-10T11:00:00",
  "return_date": null,
  "last_update": "2025-01-10T11:00:00"
}

PUT /api/v1/rentals/{id}/return → marcar alquiler como devuelto

Respuesta esperada (200 OK):

{
  "rental_id": 16050,
  "inventory_id": 1,
  "customer_id": 1,
  "staff_id": 1,
  "rental_date": "2025-01-10T11:00:00",
  "return_date": "2025-01-12T10:00:00",
  "last_update": "2025-01-12T10:00:00"
}

Errpr si ya está devuelto (400):

{
  "detail": "Rental already returned"
}


GET /api/v1/rentals/customer/{id} → alquileres de un cliente

Respuesta esperada (200 OK):

[
  {
    "rental_id": 12010,
    "inventory_id": 350,
    "customer_id": 1,
    "staff_id": 2,
    "rental_date": "2005-06-15T10:23:12",
    "return_date": "2005-06-17T12:31:00",
    "last_update": "2006-02-16T09:34:33"
  }
]


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