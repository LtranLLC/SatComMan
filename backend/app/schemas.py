from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class AccountType(str, Enum):
    Prepaid = 'Prepaid'
    Postpaid = 'Postpaid'

class AccountStatus(str, Enum):
    Active = 'Active'
    Suspended = 'Suspended'
    Closed = 'Closed'

class PaymentStatus(str, Enum):
    Paid = 'Paid'
    Unpaid = 'Unpaid'
    Overdue = 'Overdue'

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    account_type: AccountType

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    phone_number: Optional[str]
    account_status: Optional[AccountStatus]
    balance: Optional[float]

class User(UserBase):
    user_id: int
    account_status: AccountStatus
    balance: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UsageCreate(BaseModel):
    user_id: int
    call_duration: float
    data_used: float

class Usage(BaseModel):
    usage_id: int
    user_id: int
    call_duration: float
    data_used: float
    timestamp: datetime

    class Config:
        orm_mode = True

# Billing Schemas
class BillingCreate(BaseModel):
    user_id: int
    billing_period_start: datetime
    billing_period_end: datetime
    total_amount: float
    amount_due: float
    due_date: datetime
    payment_status: PaymentStatus

class Billing(BaseModel):
    bill_id: int
    user_id: int
    billing_period_start: datetime
    billing_period_end: datetime
    total_amount: float
    amount_due: float
    due_date: datetime
    payment_status: PaymentStatus

    class Config:
        orm_mode = True

# Payment Schemas
class PaymentCreate(BaseModel):
    user_id: int
    payment_date: datetime
    amount: float
    payment_method: str

class Payment(BaseModel):
    payment_id: int
    user_id: int
    payment_date: datetime
    amount: float
    payment_method: str

    class Config:
        orm_mode = True

# Device Data Schemas
class DeviceDataCreate(BaseModel):
    imei: str
    number: str
    lat: float
    lng: float
    speed: float
    heading: float
    battery_status: float
    payload: str
    usage: float
    message_id: str  # New Field
    datetime: int    # New Field (Linux epoch time)

class DeviceData(BaseModel):
    id: int
    imei: str
    number: str
    lat: float
    lng: float
    speed: float
    heading: float
    battery_status: float
    payload: str
    usage: float
    message_id: str
    datetime: int
    timestamp: datetime

    class Config:
        orm_mode = True
