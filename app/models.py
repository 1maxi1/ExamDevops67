from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class WorkshopClass(Base):
    __tablename__ = "workshop_classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)


class WorkshopRegistration(Base):
    __tablename__ = "workshop_registrations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sms_code: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    workshop_name: Mapped[str] = mapped_column(String(255), nullable=False)
    registration_time: Mapped[str] = mapped_column(String(20), nullable=False)
