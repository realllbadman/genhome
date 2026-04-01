import json
import logging

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Order
from backend.schemas import OrderCreate
from backend.services.email import send_order_customer_confirmation, send_order_owner_notification

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    c = payload.customer
    order = Order(
        first_name=c.first_name,
        last_name=c.last_name,
        phone=c.phone,
        email=c.email,
        company=c.company,
        address=c.address,
        city=c.city,
        state=c.state,
        zip=c.zip,
        contact_pref=c.contact_pref,
        best_time=c.best_time,
        notes=c.notes,
        items=json.dumps([i.model_dump() for i in payload.items]),
        total=payload.total,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    order_dict = {
        "id": order.id,
        "customer": c.model_dump(),
        "items": [i.model_dump() for i in payload.items],
        "total": payload.total,
        "created_at": str(order.created_at),
    }

    background_tasks.add_task(_send_customer_email, order_dict)
    background_tasks.add_task(_send_owner_email, order_dict)

    return {"message": "Order received successfully", "id": order.id}


async def _send_customer_email(order_dict: dict) -> None:
    try:
        await send_order_customer_confirmation(order_dict)
    except Exception:
        logger.exception("Customer order confirmation email failed for order %s", order_dict.get("id"))


async def _send_owner_email(order_dict: dict) -> None:
    try:
        await send_order_owner_notification(order_dict)
    except Exception:
        logger.exception("Owner order notification email failed for order %s", order_dict.get("id"))
