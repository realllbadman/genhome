import logging

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Booking
from backend.schemas import BookingCreate
from backend.services.email import send_customer_confirmation, send_owner_notification

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_booking(
    payload: BookingCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    booking = Booking(**payload.model_dump())
    db.add(booking)
    db.commit()
    db.refresh(booking)

    booking_dict = {
        "id": booking.id,
        "first_name": booking.first_name,
        "last_name": booking.last_name,
        "phone": booking.phone,
        "email": booking.email,
        "service": booking.service,
        "preferred_date": booking.preferred_date,
        "generator_size": booking.generator_size,
        "details": booking.details,
        "created_at": str(booking.created_at),
    }

    background_tasks.add_task(_send_customer_email, booking_dict)
    background_tasks.add_task(_send_owner_email, booking_dict)

    return {"message": "Booking received successfully", "id": booking.id}


async def _send_customer_email(booking_dict: dict) -> None:
    try:
        await send_customer_confirmation(booking_dict)
    except Exception:
        logger.exception("Customer confirmation email failed for booking %s", booking_dict.get("id"))


async def _send_owner_email(booking_dict: dict) -> None:
    try:
        await send_owner_notification(booking_dict)
    except Exception:
        logger.exception("Owner notification email failed for booking %s", booking_dict.get("id"))
