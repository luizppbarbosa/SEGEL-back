from sqlalchemy.orm import Session
from database import model

def get_all (db: Session):
    return db.query(model.Account).all()