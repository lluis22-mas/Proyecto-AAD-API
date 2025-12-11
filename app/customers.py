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
    Crear un nuevo cliente en la tabla customer.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        insert_query = """
            INSERT INTO customer (
                store_id, first_name, last_name, email,
                address_id, active, create_date, last_update
            )
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW());
        """

        values = (
            customer.store_id,
            customer.first_name,
            customer.last_name,
            customer.email,
            customer.address_id,
            customer.active,
        )

        cursor.execute(insert_query, values)
        conn.commit()

        new_id = cursor.lastrowid

        # Recuperamos el registro recién creado
        select_query = """
            SELECT customer_id, store_id, first_name, last_name,
                   email, address_id, active, create_date, last_update
            FROM customer
            WHERE customer_id = %s;
        """
        cursor.execute(select_query, (new_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row is None:
            raise HTTPException(
                status_code=500,
                detail="Error al recuperar el cliente recién creado"
            )

        return Customer(**row)

    except HTTPException:
        # Reenviamos errores HTTP (por si luego añades validaciones 400, etc.)
        raise
    except Exception as e:
        # Cualquier otra cosa es un 500
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[Customer])
def list_customers(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """
    Obtener lista de clientes con paginación básica.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT customer_id, store_id, first_name, last_name,
                   email, address_id, active, create_date, last_update
            FROM customer
            ORDER BY customer_id
            LIMIT %s OFFSET %s;
        """
        cursor.execute(query, (limit, offset))
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        customers = [Customer(**row) for row in rows]
        return customers

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    Sobrescribe todos los campos del cliente.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 1) Comprobar si el cliente existe
        cursor.execute(
            """
            SELECT customer_id
            FROM customer
            WHERE customer_id = %s;
            """,
            (customer_id,),
        )
        existing = cursor.fetchone()
        if existing is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Customer not found")

        # 2) Actualizar los campos
        update_query = """
            UPDATE customer
            SET store_id   = %s,
                first_name = %s,
                last_name  = %s,
                email      = %s,
                address_id = %s,
                active     = %s,
                last_update = NOW()
            WHERE customer_id = %s;
        """

        values = (
            data.store_id,
            data.first_name,
            data.last_name,
            data.email,
            data.address_id,
            data.active,
            customer_id,
        )

        cursor.execute(update_query, values)
        conn.commit()

        # 3) Volver a leer el cliente actualizado
        cursor.execute(
            """
            SELECT customer_id, store_id, first_name, last_name,
                   email, address_id, active, create_date, last_update
            FROM customer
            WHERE customer_id = %s;
            """,
            (customer_id,),
        )
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row is None:
            # Algo raro ha pasado si aquí no encontramos el registro
            raise HTTPException(
                status_code=500,
                detail="Error al recuperar el cliente actualizado"
            )

        return Customer(**row)

    except HTTPException:
        # Reenviamos 404 tal cual
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{customer_id}", status_code=204)
def delete_customer(customer_id: int):
    """
    Eliminar un cliente por ID.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        delete_query = """
            DELETE FROM customer
            WHERE customer_id = %s;
        """
        cursor.execute(delete_query, (customer_id,))
        conn.commit()

        filas_afectadas = cursor.rowcount

        cursor.close()
        conn.close()

        if filas_afectadas == 0:
            # No se ha borrado nada → no existía
            raise HTTPException(status_code=404, detail="Customer not found")

        # 204 No Content → no devolvemos body
        return

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
