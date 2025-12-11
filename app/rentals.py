from fastapi import APIRouter, HTTPException, Query
from typing import List
from .db import get_connection
from .schemas import Rental, RentalCreate

router = APIRouter(
    prefix="/api/v1/rentals",
    tags=["rentals"],
)

@router.post("", response_model=Rental, status_code=201)
def create_rental(rental: RentalCreate):
    """
    Crear un nuevo alquiler en la tabla rental.
    Comprobar:
    - que el inventario existe
    - que el cliente existe
    - que el empleado (staff) existe
    - que el inventario no está ya alquilado (rental sin return_date)
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 1) Comprobar que el inventory existe
        cursor.execute(
            "SELECT inventory_id FROM inventory WHERE inventory_id = %s;",
            (rental.inventory_id,),
        )
        inv = cursor.fetchone()
        if inv is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Inventory not found")

        # 2) Comprobar que el customer existe
        cursor.execute(
            "SELECT customer_id FROM customer WHERE customer_id = %s;",
            (rental.customer_id,),
        )
        cust = cursor.fetchone()
        if cust is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Customer not found")

        # 3) Comprobar que el staff existe
        cursor.execute(
            "SELECT staff_id FROM staff WHERE staff_id = %s;",
            (rental.staff_id,),
        )
        staff = cursor.fetchone()
        if staff is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Staff not found")

        # 4) Comprobar que el inventario NO está actualmente alquilado
        # (rental con ese inventory_id y return_date IS NULL)
        cursor.execute(
            """
            SELECT rental_id
            FROM rental
            WHERE inventory_id = %s
              AND return_date IS NULL;
            """,
            (rental.inventory_id,),
        )
        existing_rental = cursor.fetchone()
        if existing_rental is not None:
            cursor.close()
            conn.close()
            raise HTTPException(
                status_code=400,
                detail="Inventory is already rented (open rental exists)",
            )

        # 5) Insertar el nuevo rental
        insert_query = """
            INSERT INTO rental (
                rental_date,
                inventory_id,
                customer_id,
                return_date,
                staff_id,
                last_update
            )
            VALUES (NOW(), %s, %s, NULL, %s, NOW());
        """

        values = (
            rental.inventory_id,
            rental.customer_id,
            rental.staff_id,
        )

        cursor.execute(insert_query, values)
        conn.commit()

        new_id = cursor.lastrowid

        # 6) Recuperar el rental recién creado
        select_query = """
            SELECT rental_id, inventory_id, customer_id, staff_id,
                   rental_date, return_date, last_update
            FROM rental
            WHERE rental_id = %s;
        """
        cursor.execute(select_query, (new_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row is None:
            raise HTTPException(
                status_code=500,
                detail="Error al recuperar el rental recién creado",
            )

        return Rental(**row)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- ENDPOINTS ESQUELETO (los completaremos luego) ----------

@router.get("", response_model=List[Rental])
def list_rentals(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """
    Listar rentals con paginación.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT rental_id, inventory_id, customer_id, staff_id,
                   rental_date, return_date, last_update
            FROM rental
            ORDER BY rental_date DESC, rental_id DESC
            LIMIT %s OFFSET %s;
        """
        cursor.execute(query, (limit, offset))
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        rentals = [Rental(**row) for row in rows]
        return rentals

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{rental_id}", response_model=Rental)
def get_rental(rental_id: int):
    """
    Obtener detalle de un rental por ID.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT rental_id, inventory_id, customer_id, staff_id,
                   rental_date, return_date, last_update
            FROM rental
            WHERE rental_id = %s;
        """
        cursor.execute(query, (rental_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row is None:
            raise HTTPException(status_code=404, detail="Rental not found")

        return Rental(**row)

    except HTTPException:
        # reenviamos 404 tal cual
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.put("/{rental_id}/return", response_model=Rental)
def return_rental(rental_id: int):
    """
    Marcar un rental como devuelto (set return_date = NOW()).
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 1) Comprobar que existe
        cursor.execute(
            """
            SELECT rental_id, return_date
            FROM rental
            WHERE rental_id = %s;
            """,
            (rental_id,),
        )
        rental = cursor.fetchone()

        if rental is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Rental not found")

        # 2) Comprobar que NO está devuelto
        if rental["return_date"] is not None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Rental already returned")

        # 3) Marcar como devuelto
        cursor.execute(
            """
            UPDATE rental
            SET return_date = NOW(), last_update = NOW()
            WHERE rental_id = %s;
            """,
            (rental_id,),
        )
        conn.commit()

        # 4) Recuperar rental actualizado
        cursor.execute(
            """
            SELECT rental_id, inventory_id, customer_id, staff_id,
                   rental_date, return_date, last_update
            FROM rental
            WHERE rental_id = %s;
            """,
            (rental_id,),
        )
        updated = cursor.fetchone()

        cursor.close()
        conn.close()

        return Rental(**updated)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/customer/{customer_id}", response_model=List[Rental])
def list_rentals_by_customer(
    customer_id: int,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """
    Listar todos los rentals asociados a un cliente.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 1) Comprobar que el cliente existe
        cursor.execute(
            "SELECT customer_id FROM customer WHERE customer_id = %s;",
            (customer_id,),
        )
        exists = cursor.fetchone()

        if exists is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Customer not found")

        # 2) Obtener los rentals del cliente
        query = """
            SELECT rental_id, inventory_id, customer_id, staff_id,
                   rental_date, return_date, last_update
            FROM rental
            WHERE customer_id = %s
            ORDER BY rental_date DESC, rental_id DESC
            LIMIT %s OFFSET %s;
        """
        cursor.execute(query, (customer_id, limit, offset))
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        rentals = [Rental(**row) for row in rows]
        return rentals

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

