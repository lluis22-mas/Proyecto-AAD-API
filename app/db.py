import os
from mysql.connector import pooling, Error
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

dbconfig = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3305")),  # tu puerto en Heidi
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "1234"),
    "database": os.getenv("DB_NAME", "sakila"),
}

connection_pool = None  # se rellenará en init_pool()


def init_pool():
    """
    Crea el pool de conexiones si aún no existe.
    """
    global connection_pool
    if connection_pool is None:
        try:
            print("Creando pool de conexiones...")
            connection_pool = pooling.MySQLConnectionPool(
                pool_name="sakila_pool",
                pool_size=5,
                **dbconfig
            )
            print("Pool de conexiones creado correctamente")
        except Error as e:
            print(f"Error creando el pool de conexiones: {e}")
            raise


def get_connection():
    """
    Devuelve una conexión activa del pool.
    Lanza error claro si algo falla.
    """
    global connection_pool

    if connection_pool is None:
        init_pool()

    conn = connection_pool.get_connection()

    if conn is None:
        raise RuntimeError("No se ha podido obtener una conexión del pool (conn es None)")

    return conn
