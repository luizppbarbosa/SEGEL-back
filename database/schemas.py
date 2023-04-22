from pydantic import BaseModel, Field
import datetime

class ReservationBase(BaseModel):
    value: int
    reservation_date: str
    time_start: str
    time_end: str
    justification: str
    reservation_type: str
    status: str   

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    area_id: str
    account_id: str

    class Config:
        orm_mode = True


class ReservationUpdate(BaseModel):
    value: int
    reservation_date: str
    time_start: str
    time_end: str
    justification: str
    reservation_type: str
    status: str
    area_id: str
    account_id: str

class AreaBase(BaseModel):
    name: str

class AreaCreate(AreaBase):
    pass

class Area(AreaBase):
    description: str
    available: bool
    account_id: str | None = None

    reservations = list[Reservation]

    class Config:
        orm_mode = True

class AreaUpdate(BaseModel):
    name: str 
    description: str 
    available: bool 
    account_id: str

    class Config:
        orm_mode = True

class AreaDelete(BaseModel):
    name: str 
    description: str 
    available: bool
    account_id: str

    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    id: str
    email: str

class AccountCreate(AccountBase):
    password: str

class Account(AccountBase):
    cpf: str
    name: str
    email: str
    hashed_password: str
    user_type: str
    available: bool
    phone_number: str
    

    reservations = list[Reservation]
    areas = list[Area]
    
    
    class Config:
        orm_mode = True

class AccountUpdate(BaseModel):
    name: str
    email: str
    hashed_password: str
    phone_number: str
    
    class Config:
        orm_mode = True

class AccountDelete(BaseModel):
    available: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: object


class TokenData(BaseModel):
    email: str | None = None


class AccountInDB(Account):
    hashed_password: str