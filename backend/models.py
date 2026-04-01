from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Text, DateTime, Float
from backend.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    service = Column(Text, nullable=False)
    preferred_date = Column(Text, nullable=True)
    generator_size = Column(Text, nullable=True)
    details = Column(Text, nullable=True)
    status = Column(Text, default="pending", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    notes = Column(Text, nullable=True)


class Order(Base):
    __tablename__ = "orders"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    first_name   = Column(Text, nullable=False)
    last_name    = Column(Text, nullable=False)
    phone        = Column(Text, nullable=False)
    email        = Column(Text, nullable=False)
    company      = Column(Text, nullable=True)
    address      = Column(Text, nullable=True)
    city         = Column(Text, nullable=True)
    state        = Column(Text, nullable=True)
    zip          = Column(Text, nullable=True)
    contact_pref = Column(Text, nullable=True)
    best_time    = Column(Text, nullable=True)
    notes        = Column(Text, nullable=True)
    items        = Column(Text, nullable=False)   # JSON string
    total        = Column(Float, nullable=False)
    status       = Column(Text, default="pending", nullable=False)
    created_at   = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
