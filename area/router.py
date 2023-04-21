from typing import List
from fastapi import Depends, Query
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from database import schemas
from area import manager
from database.database import get_db


router = APIRouter(
    prefix="/area",
    tags=["Area"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=schemas.Area)
def create_area(area: schemas.Area, db: Session = Depends(get_db)):
    db_area = manager.get_area_by_name(db, name=area.name)
    if db_area:
        raise HTTPException(
            status_code=400, detail="Area already registered")
    return manager.create_area(db=db, area=area)


@router.get("/list", response_model=List[schemas.Area])
def read_users(db: Session = Depends(get_db)):
    users = manager.get_all(db)
    return users


@router.put("/update/{area_id}", response_model=schemas.Area)
def update_area(area_id: str, area: schemas.AreaUpdate, db: Session = Depends(get_db)):
    match_user = manager.get_user_by_id(db, id=area.account_id)
    db_area = manager.get_area_by_id(db, id=area_id)
    if match_user == False:
        raise HTTPException(
            status_code=404, detail="User not found or unauthorized user")
    if not db_area:
        raise HTTPException(
            status_code=404, detail="Area not found")
    updated_area = manager.update_area(db=db, area=area, db_area=db_area)
    return updated_area



'''@router.put("/updatedell/{area_id}", response_model=schemas.Area)
def delete_area_update(area_id: str, area: schemas.AreaDelete, db: Session = Depends(get_db)):
    db_area = manager.get_area_by_id(db, id=area_id)
    if not db_area:
        raise HTTPException(
            status_code=404, detail="Area not found")
    delete_area_update = manager.delete_area_update(db=db, area=area, db_area=db_area)
    return delete_area_update


@router.delete("/delete/{area_id}")
def delete_area(area_id: str, db: Session = Depends(get_db)):
    db_area = manager.get_area_by_id(db, id=area_id)
    if not db_area:
        raise HTTPException(
            status_code=404, detail="Area not found")
    manager.delete_area(db=db, db_area=db_area)
    return {"message": "Area deleted"}'''


@router.delete("/delete/{area_id}", response_model=schemas.Area)
def area_delete_or_update(area_id: str, db: Session = Depends(get_db)):
    db_area = manager.get_area_by_id(db, id=area_id)
    if not db_area:
        raise HTTPException(
            status_code=404, detail="Area not found")
    count = manager.get_area_reservations(area_id = area_id, db=db)
    if count > 0:
        delete_area_update = manager.delete_area_update(db=db, db_area=db_area)
        return delete_area_update
    else:
        result = manager.delete_area(db=db, db_area=db_area)
        return result