from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from database import schemas
from account import manager
from database.database import get_db
from auth.manager import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["user"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@router.get("/list", response_model=List[schemas.Account])
def read_users(db: Session = Depends(get_db)):
    users = manager.get_all(db)
    return users