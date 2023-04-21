from sqlalchemy.orm import Session
import uuid
from fastapi import HTTPException
from database import model, schemas
# from sheets.manager import execute


def get_all(db: Session):
    return db.query(model.Reservation).all()


def create_reservation(db: Session, reservation: schemas.Reservation):

    user = db.query(model.Account).filter(
        model.Account.id == reservation.account_id).first()

    area = db.query(model.Area).filter(
        model.Area.id == reservation.area_id).first()

    if user and area:

        db_order = model.Reservation(
            id=uuid.uuid4().hex,
            value=reservation.value,
            reservation_date=reservation.reservation_date,
            time_start=reservation.time_start,
            time_end=reservation.time_end,
            justification=reservation.justification,
            user_type=reservation.user_type,
            status=reservation.status,
            area_id=reservation.area_id,
            account_id=reservation.account_id
        )

        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        # execute()

        return db_order
    else:
        return None


def get_reservation_by_id(db: Session, reservation_id: str):
    return db.query(model.Reservation).filter(model.Reservation.id == reservation_id).first()

def update_reservation(db: Session, reservation: schemas.ReservationUpdate, db_reservation = model.Reservation):
    #if not db_reservation:
        #return None
    if reservation.value:
        db_reservation.value = reservation.value
    if reservation.reservation_date:
        db_reservation.reservation_date = reservation.reservation_date
    if reservation.time_start:
        db_reservation.time_start = reservation.time_start
    if reservation.time_end:
        db_reservation.time_end = reservation.time_end
    if reservation.justification:
        db_reservation.justification = reservation.justification
    if reservation.user_type:
        db_reservation.user_type = reservation.user_type
    if reservation.status:
        db_reservation.status = reservation.status
    if reservation.account_id:
        db_reservation.account_id = reservation.account_id
    if reservation.area_id:
        db_reservation.area_id = reservation.area_id
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


def delete_reservation(db: Session, db_reservation: model.Reservation):
    db.delete(db_reservation)
    db.commit()

'''def delete_reservation(db: Session, reservation_id: int):
    db_reservation = get_reservation_by_id(db, reservation_id=reservation_id)
    if not db_reservation:
        return None
    db.delete(db_reservation)
    db.commit()
    return db_reservation'''