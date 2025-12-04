from fastapi import FastAPI, HTTPException
from .db import get_connection
from .customers import router as customers_router

app = FastAPI(title="Sakila API", version="1.0.0")

# Registrar rutas de customers
app.include_router(customers_router)

@app.get("/health")
def health_check():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return {"status": "ok", "db": row[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
