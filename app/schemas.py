from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# ---------------------------
# SCHEMAS PARA CUSTOMERS
# ---------------------------

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    address_id: int
    store_id: int
    active: int = 1

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase):
    customer_id: int
    create_date: datetime
    last_update: Optional[datetime]

    class Config:
        from_attributes = True


# ---------------------------
# SCHEMAS PARA RENTALS
# ---------------------------

class RentalBase(BaseModel):
    inventory_id: int
    customer_id: int
    staff_id: int

class RentalCreate(RentalBase):
    pass

class Rental(RentalBase):
    rental_id: int
    rental_date: datetime
    return_date: Optional[datetime]
    last_update: datetime

    class Config:
        from_attributes = True
