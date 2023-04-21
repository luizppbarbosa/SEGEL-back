from sqlalchemy.orm import Session
import uuid
from database import model, schemas


def get_area_by_name(db: Session, name: str):
    return db.query(model.Area).filter(model.Area.name == name).first()


def get_all(db: Session):
    return db.query(model.Area).all()

area_counter = 1

def create_area(db: Session, area: schemas.Area):

    global area_counter

    user = db.query(model.Account).filter(
        model.Account.id == area.account_id).first()

    if not user:
        area.account_id = None

    else:
        area.account_id = user.id

    db_area = model.Area(
        id=str(area_counter),
        name=area.name,
        description=area.description,
        available=area.available,
        account_id=area.account_id
    )

    db.add(db_area)
    db.commit()
    db.refresh(db_area)

    area_counter += 1

    # execute()

    return db_area


def get_area_by_id(db: Session, id: str):
    return db.query(model.Area).filter(model.Area.id == id).first()

def get_user_by_id(db: Session, id: str):
    find_user = db.query(model.Account).filter(model.Account.id == id).first()
    if not find_user:
        return False
    elif find_user and find_user.user_type == "0":
        return True   
    return False

def update_area(db: Session, area: schemas.AreaUpdate, db_area: model.Area):
    if area.name:
        db_area.name = area.name
    if area.description:
        db_area.description = area.description

    db_area.available = area.available
    
    db.commit()
    db.refresh(db_area)
    return db_area


# Exclui tudo
def delete_area(db: Session, db_area: model.Area):
    db.delete(db_area)
    db.commit()
    return db_area


def delete_area_update(db: Session, db_area: model.Area):
    '''if not db_area:
        return None'''
    db_area.available = False
    db.commit()
    db.refresh(db_area)
    return db_area


def get_area_reservations(area_id: str, db: Session):
    return db.query(model.Reservation).filter(model.Reservation.area_id == area_id).count()