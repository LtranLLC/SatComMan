from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, UniqueConstraint, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class AccountType(str, enum.Enum):
    Prepaid = 'Prepaid'
    Postpaid = 'Postpaid'

class AccountStatus(str, enum.Enum):
    Active = 'Active'
    Suspended = 'Suspended'
    Closed = 'Closed'

class PaymentStatus(str, enum.Enum):
    Paid = 'Paid'
    Unpaid = 'Unpaid'
    Overdue = 'Overdue'

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    phone_number = Column(String(20), unique=True, index=True)
    imei = Column(String(50), unique=True, index=True)  # New Field
    hashed_password = Column(String(255))
    account_type = Column(Enum(AccountType))
    account_status = Column(Enum(AccountStatus), default=AccountStatus.Active)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    usage = relationship("Usage", back_populates="user")
    billing = relationship("Billing", back_populates="user")
    payments = relationship("Payment", back_populates="user")

class Usage(Base):
    __tablename__ = 'usage'
    usage_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    call_duration = Column(Float, default=0.0)  # in minutes
    data_used = Column(Float, default=0.0)      # in MB
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="usage")

class Billing(Base):
    __tablename__ = 'billing'
    bill_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    billing_period_start = Column(DateTime)
    billing_period_end = Column(DateTime)
    total_amount = Column(Float)
    amount_due = Column(Float)
    due_date = Column(DateTime)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.Unpaid)
    user = relationship("User", back_populates="billing")

class Payment(Base):
    __tablename__ = 'payments'
    payment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    payment_date = Column(DateTime, default=datetime.utcnow)
    amount = Column(Float)
    payment_method = Column(String(50))
    user = relationship("User", back_populates="payments")

class DeviceData(Base):
    __tablename__ = 'device_data'
    id = Column(Integer, primary_key=True, index=True)
    imei = Column(String(50), index=True)
    number = Column(String(20))
    lat = Column(Float)
    lng = Column(Float)
    speed = Column(Float)
    heading = Column(Float)
    battery_status = Column(Float)
    payload = Column(String(255))
    usage = Column(Float)
    message_id = Column(String(100), unique=True)  # New Field with Unique Constraint
    datetime = Column(BigInteger)     # New Field (Linux epoch time)
    timestamp = Column(DateTime, default=datetime.utcnow)
