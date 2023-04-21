from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(String, primary_key=True, index=True)
    cpf = Column(String, unique=True, index=False)
    name = Column(String, unique=False, index=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    user_type = Column(String)
    available = Column(Boolean)
    phone_number = Column(String)

    reservations = relationship("Reservation", back_populates="account")
    areas = relationship("Area", back_populates="account")


class Area(Base):
    __tablename__ = "areas"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=False)
    available = Column(Boolean)
    description = Column(String)
    account_id = Column(String, ForeignKey("accounts.id"), nullable=True)

    account = relationship("Account", back_populates="areas")
    reservations = relationship("Reservation", back_populates="areas")


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(String, primary_key=True, index=True)
    value = Column(Integer)
    reservation_date = Column(DateTime)
    time_start = Column(String)
    time_end = Column(String)
    justification = Column(String)
    user_type = Column(String)
    status = Column(String)
    area_id = Column(String, ForeignKey("areas.id"))
    account_id = Column(String, ForeignKey("accounts.id"))

    account = relationship("Account", back_populates="reservations")
    areas = relationship("Area", back_populates="reservations")