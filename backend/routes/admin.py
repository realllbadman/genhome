import os
import secrets
from datetime import datetime, timezone
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Booking, Order
from backend.schemas import BookingOut, BookingUpdate, OrderOut, OrderUpdate

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme123")

router = APIRouter()
security = HTTPBasic()


def require_admin(credentials: HTTPBasicCredentials = Depends(security)):
    ok_user = secrets.compare_digest(credentials.username.encode(), ADMIN_USERNAME.encode())
    ok_pass = secrets.compare_digest(credentials.password.encode(), ADMIN_PASSWORD.encode())
    if not (ok_user and ok_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )


# ── List bookings ─────────────────────────────────────────────────────────────

@router.get("/bookings", response_model=List[BookingOut], dependencies=[Depends(require_admin)])
def list_bookings(
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Booking)

    if status:
        query = query.filter(Booking.status == status)

    if search:
        term = f"%{search.lower()}%"
        query = query.filter(
            func.lower(Booking.first_name).like(term)
            | func.lower(Booking.last_name).like(term)
            | func.lower(Booking.email).like(term)
        )

    return query.order_by(Booking.created_at.desc()).all()


# ── Single booking ────────────────────────────────────────────────────────────

@router.get("/bookings/{booking_id}", response_model=BookingOut, dependencies=[Depends(require_admin)])
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return booking


# ── Update booking ────────────────────────────────────────────────────────────

@router.patch("/bookings/{booking_id}", response_model=BookingOut, dependencies=[Depends(require_admin)])
def update_booking(booking_id: int, payload: BookingUpdate, db: Session = Depends(get_db)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(booking, field, value)

    db.commit()
    db.refresh(booking)
    return booking


# ── Delete booking ────────────────────────────────────────────────────────────

@router.delete("/bookings/{booking_id}", dependencies=[Depends(require_admin)])
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted"}


# ── Orders ────────────────────────────────────────────────────────────────────

@router.get("/orders", response_model=List[OrderOut], dependencies=[Depends(require_admin)])
def list_orders(
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Order)
    if status:
        query = query.filter(Order.status == status)
    if search:
        term = f"%{search.lower()}%"
        query = query.filter(
            func.lower(Order.first_name).like(term)
            | func.lower(Order.last_name).like(term)
            | func.lower(Order.email).like(term)
        )
    return query.order_by(Order.created_at.desc()).all()


@router.get("/orders/{order_id}", response_model=OrderOut, dependencies=[Depends(require_admin)])
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.patch("/orders/{order_id}", response_model=OrderOut, dependencies=[Depends(require_admin)])
def update_order(order_id: int, payload: OrderUpdate, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(order, field, value)
    db.commit()
    db.refresh(order)
    return order


@router.delete("/orders/{order_id}", dependencies=[Depends(require_admin)])
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted"}


# ── Stats ─────────────────────────────────────────────────────────────────────

@router.get("/stats", dependencies=[Depends(require_admin)])
def get_stats(db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    total_quotes   = db.query(func.count(Booking.id)).scalar()
    pending_quotes = db.query(func.count(Booking.id)).filter(Booking.status == "pending").scalar()
    total_orders   = db.query(func.count(Order.id)).scalar()
    pending_orders = db.query(func.count(Order.id)).filter(Order.status == "pending").scalar()
    orders_month   = db.query(func.count(Order.id)).filter(Order.created_at >= month_start).scalar()

    return {
        "total_quotes":   total_quotes,
        "pending_quotes": pending_quotes,
        "total_orders":   total_orders,
        "pending_orders": pending_orders,
        "orders_month":   orders_month,
    }
