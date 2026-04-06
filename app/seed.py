from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import MetroChange, TravelCard

DEFAULT_METRO_CHANGES = [
    {
        "id": 1,
        "description": "Закрытие станции Рижская",
        "affected_line": "Калужско-рижская",
    },
    {
        "id": 2,
        "description": "Проезд поездов только по часовой стрелке с 1 января",
        "affected_line": "Кольцевая",
    },
    {
        "id": 3,
        "description": "Закрытие станции Проспект Вернадского",
        "affected_line": "Сокольническая",
    },
]

DEFAULT_TRAVEL_CARDS = [
    {
        "id": 1,
        "phone": "+79846274627",
        "sms_code": "1420",
        "balance": 100,
        "last_entry_station": "Юго-западная",
    },
    {
        "id": 2,
        "phone": "+79175628572",
        "sms_code": "1100",
        "balance": 50,
        "last_entry_station": "Автозаводская",
    },
    {
        "id": 3,
        "phone": "+7916552451",
        "sms_code": "1100",
        "balance": 51,
        "last_entry_station": "Коломенская",
    },
]


def seed_initial_data(session: Session) -> None:
    has_metro_changes = session.scalar(select(MetroChange.id).limit(1))
    has_travel_cards = session.scalar(select(TravelCard.id).limit(1))

    if not has_metro_changes:
        session.add_all(MetroChange(**change_data) for change_data in DEFAULT_METRO_CHANGES)

    if not has_travel_cards:
        session.add_all(TravelCard(**card_data) for card_data in DEFAULT_TRAVEL_CARDS)

    session.commit()
