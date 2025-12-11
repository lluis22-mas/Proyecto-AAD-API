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
