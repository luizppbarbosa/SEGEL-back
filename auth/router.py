from datetime import timedelta
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from database import schemas, model
from fastapi.security import OAuth2PasswordRequestForm
from auth import manager
from database.database import get_db


router = APIRouter(
    prefix="/account",
    tags=["Account"],
    responses={404: {"description": "Not found"}},
)



@router.post("/sign-in", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = manager.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=manager.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = manager.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "user": user}


@router.post("/create", response_model=schemas.Account)
def create_account(account: schemas.Account, db: Session = Depends(get_db)):
    db_account = manager.get_account_by_email(db, email=account.email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    return manager.create_account(db=db, account=account)


@router.put("/update/{account_id}", response_model=schemas.Account)
def update_account(account_id: str, account: schemas.AccountUpdate, db: Session = Depends(get_db)):
    db_account = manager.get_account_by_id(db, account_id)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    updated_account = manager.update_account(db=db, db_account=db_account, account=account)
    return updated_account


@router.delete("/delete/{account_id}", response_model=schemas.Account)
def area_delete_or_update(account_id: str, account: schemas.AccountDelete, db: Session = Depends(get_db)):
    db_account = manager.get_account_by_id(db, account_id=account_id)
    if not db_account:
        raise HTTPException(
            status_code=404, detail="Account not found")
    count = manager.get_account_reservations(account_id = account_id, db=db)
    if count > 0:
        result = manager.delete_account_update(db=db, db_account=db_account)
        return result
    else:
        result = manager.delete_account(db=db, db_account=db_account)
        return result