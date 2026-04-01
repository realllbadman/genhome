from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class BookingCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: EmailStr
    service: str
    preferred_date: Optional[str] = None
    generator_size: Optional[str] = None
    details: Optional[str] = None


class OrderCustomer(BaseModel):
    first_name:   str
    last_name:    str
    phone:        str
    email:        EmailStr
    company:      Optional[str] = None
    address:      Optional[str] = None
    city:         Optional[str] = None
    state:        Optional[str] = None
    zip:          Optional[str] = None
    contact_pref: Optional[str] = None
    best_time:    Optional[str] = None
    notes:        Optional[str] = None


class OrderItem(BaseModel):
    product_id: str
    name:       str
    kw:         Optional[float] = None
    fuel:       Optional[str] = None
    unit_price: float
    quantity:   int


class OrderCreate(BaseModel):
    customer: OrderCustomer
    items:    List[OrderItem]
    total:    float


class BookingUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


class OrderOut(BaseModel):
    id:           int
    first_name:   str
    last_name:    str
    phone:        str
    email:        str
    company:      Optional[str] = None
    address:      Optional[str] = None
    city:         Optional[str] = None
    state:        Optional[str] = None
    zip:          Optional[str] = None
    contact_pref: Optional[str] = None
    best_time:    Optional[str] = None
    notes:        Optional[str] = None
    items:        str   # JSON string
    total:        float
    status:       str
    created_at:   datetime

    class Config:
        from_attributes = True


class BookingOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str
    email: str
    service: str
    preferred_date: Optional[str] = None
    generator_size: Optional[str] = None
    details: Optional[str] = None
    status: str
    created_at: datetime
    notes: Optional[str] = None

    class Config:
        from_attributes = True
