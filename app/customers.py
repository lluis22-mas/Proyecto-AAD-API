from fastapi import APIRouter, HTTPException, Query
from typing import List
from .db import get_connection
from .schemas import Customer, CustomerCreate, CustomerUpdate

router = APIRouter(
    prefix="/api/v1/customers",
    tags=["customers"],
)

@router.post("", response_model=Customer, status_code=201)
def create_customer(customer: CustomerCreate):
    """
    Crear un nuevo cliente.
    (Implementaremos la lógica SQL en el siguiente bloque)
    """
    raise HTTPException(status_code=501, detail="Not implemented yet")

@router.get("", response_model=List[Customer])
def list_customers(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """
    Obtener lista de clientes con paginación básica.
    """
    raise HTTPException(status_code=501, detail="Not implemented yet")

@router.get("/{customer_id}", response_model=Customer)
def get_customer(customer_id: int):
    """
    Obtener detalle de un cliente por ID.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT customer_id, store_id, first_name, last_name,
                   email, address_id, active, create_date, last_update
            FROM customer
            WHERE customer_id = %s;
        """
        cursor.execute(query, (customer_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row is None:
            raise HTTPException(status_code=404, detail="Customer not found")

        return Customer(**row)

    except HTTPException:
        # Re-lanzamos los errores 404 tal cual
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.put("/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, data: CustomerUpdate):
    """
    Actualizar un cliente por ID.
    """
    raise HTTPException(status_code=501, detail="Not implemented yet")

@router.delete("/{customer_id}", status_code=204)
def delete_customer(customer_id: int):
    """
    Eliminar un cliente por ID.
    """
    raise HTTPException(status_code=501, detail="Not implemented yet")
