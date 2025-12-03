from fastapi import FastAPI, HTTPException
from .db import get_connection

app = FastAPI(title="Sakila API", version="1.0.0")

@app.get("/health")
def health_check():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Consulta sencilla para comprobar la conexión
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return {"status": "ok", "db": result[0]}
    except Exception as e:
        # Si hay cualquier problema con la BD, devolvemos 500
        raise HTTPException(status_code=500, detail=str(e))
