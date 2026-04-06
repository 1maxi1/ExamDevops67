from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class MetroChange(Base):
    __tablename__ = "metro_changes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    affected_line: Mapped[str] = mapped_column(String(100), nullable=False)


class TravelCard(Base):
    __tablename__ = "travel_cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    sms_code: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    balance: Mapped[int] = mapped_column(Integer, nullable=False)
    last_entry_station: Mapped[str] = mapped_column(String(100), nullable=False)
