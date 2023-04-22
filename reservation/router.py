from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from database import schemas
from reservation import manager
from database.database import get_db
from auth.manager import get_current_user

router = APIRouter(
    prefix="/reservations",
    tags=["Reservation"],
    responses={404: {"description": "Not found"}},
)


# @router.post("/create", response_model=schemas.Reservation)
# def create_reservation(reservation: schemas.Reservation, db: Session = Depends(get_db)):
#     result = manager.create_reservation(db=db, reservation=reservation)
#     if result == None:
#         raise HTTPException(
#             status_code=400, detail="User or Area doesn't exist try again.")
#     return result

@router.post("/create", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.Reservation, db: Session = Depends(get_db)):
    
    reserva_solicitada = manager.convert_datetime(reservation)

    if reserva_solicitada[0] > reserva_solicitada[1]:
        raise HTTPException(
            status_code=400, detail="Time start is higher than time end")

    existing_reservations = manager.get_all(db)
    
    for reservas in existing_reservations:
        reservas_feitas = manager.convert_datetime(reservas)
        
        if (reservas_feitas[0] == reserva_solicitada[0] and reservas_feitas[1] == reserva_solicitada[1]) or (reservas_feitas[0] < reserva_solicitada[0] < reservas_feitas[1] or reservas_feitas[0] < reserva_solicitada[1] < reservas_feitas[1]):
            raise HTTPException(
            status_code=400, detail="Reservation date or hour already in use")


    result = manager.create_reservation(db=db, reservation=reservation)
    if result == None:
        raise HTTPException(
            status_code=400, detail="User or Area doesn't exist try again.")
    
    return result


@router.get("/list", response_model=List[schemas.Reservation])
def read_users(db: Session = Depends(get_db)):
    orders = manager.get_all(db)
    return orders


@router.put("/update/{reservation_id}", response_model=schemas.Reservation)
def update_reservation(reservation_id: str, reservation: schemas.ReservationUpdate, db: Session = Depends(get_db)):
    db_reservation = manager.get_reservation_by_id(db, reservation_id=reservation_id)
    if not db_reservation:
        raise HTTPException(
            status_code=404, detail="Reservation not found")
    updated_reservation = manager.update_reservation(db=db, db_reservation=db_reservation, reservation=reservation)
    return updated_reservation



@router.delete("/delete/{reservation_id}")
def delete_reservation(reservation_id: str, db: Session = Depends(get_db)):
    db_reservation = manager.get_reservation_by_id(db, reservation_id=reservation_id)
    if not db_reservation:
        raise HTTPException(
            status_code=404, detail="Reservation not found")
    manager.delete_reservation(db=db, db_reservation = db_reservation)
    return {"message": "Reservation successfully deleted"}