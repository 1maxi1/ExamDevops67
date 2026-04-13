from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import WorkshopClass, WorkshopRegistration

DEFAULT_WORKSHOP_CLASSES = [
    {
        "id": 1,
        "name": "Гончарный круг",
        "price": 3500,
    },
    {
        "id": 2,
        "name": "Лепим жабу",
        "price": 2500,
    },
    {
        "id": 3,
        "name": "Лепим вазу",
        "price": 2800,
    },
]

DEFAULT_WORKSHOP_REGISTRATIONS = [
    {
        "id": 1,
        "sms_code": "1871",
        "workshop_name": "Гончарный круг",
        "registration_time": "18:10",
    },
    {
        "id": 2,
        "sms_code": "1671",
        "workshop_name": "Лепим жабу",
        "registration_time": "12:20",
    },
    {
        "id": 3,
        "sms_code": "1471",
        "workshop_name": "Лепим вазу",
        "registration_time": "11:05",
    },
]


def seed_initial_data(session: Session) -> None:
    has_workshop_classes = session.scalar(select(WorkshopClass.id).limit(1))
    has_registrations = session.scalar(select(WorkshopRegistration.id).limit(1))

    if not has_workshop_classes:
        session.add_all(WorkshopClass(**class_data) for class_data in DEFAULT_WORKSHOP_CLASSES)

    if not has_registrations:
        session.add_all(
            WorkshopRegistration(**registration_data)
            for registration_data in DEFAULT_WORKSHOP_REGISTRATIONS
        )

    session.commit()
