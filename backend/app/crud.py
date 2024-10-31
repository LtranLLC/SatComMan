from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from . import models, schemas
from datetime import datetime

def get_user(db: Session, user_id: int):
    try:
        return db.query(models.User).filter(models.User.user_id == user_id).first()
    except SQLAlchemyError as e:
        raise e

def get_user_by_email(db: Session, email: str):
    try:
        return db.query(models.User).filter(models.User.email == email).first()
    except SQLAlchemyError as e:
        raise e

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    try:
        db_user = models.User(
            name=user.name,
            email=user.email,
            phone_number=user.phone_number,
            account_type=user.account_type,
            hashed_password=hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    try:
        db_user = get_user(db, user_id)
        if db_user:
            for key, value in user.dict(exclude_unset=True).items():
                setattr(db_user, key, value)
            db_user.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def delete_user(db: Session, user_id: int):
    try:
        db_user = get_user(db, user_id)
        if db_user:
            db.delete(db_user)
            db.commit()
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def add_usage(db: Session, usage: schemas.UsageCreate):
    try:
        db_usage = models.Usage(
            user_id=usage.user_id,
            call_duration=usage.call_duration,
            data_used=usage.data_used,
            timestamp=datetime.utcnow()
        )
        db.add(db_usage)
        db.commit()
        db.refresh(db_usage)
        return db_usage
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def get_usage_by_user(db: Session, user_id: int):
    try:
        return db.query(models.Usage).filter(models.Usage.user_id == user_id).all()
    except SQLAlchemyError as e:
        raise e

def create_billing(db: Session, billing: schemas.BillingCreate):
    try:
        db_billing = models.Billing(
            user_id=billing.user_id,
            billing_period_start=billing.billing_period_start,
            billing_period_end=billing.billing_period_end,
            total_amount=billing.total_amount,
            amount_due=billing.amount_due,
            due_date=billing.due_date,
            payment_status=billing.payment_status
        )
        db.add(db_billing)
        db.commit()
        db.refresh(db_billing)
        return db_billing
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def get_billing_by_user(db: Session, user_id: int):
    try:
        return db.query(models.Billing).filter(models.Billing.user_id == user_id).all()
    except SQLAlchemyError as e:
        raise e

def make_payment(db: Session, payment: schemas.PaymentCreate):
    try:
        db_payment = models.Payment(
            user_id=payment.user_id,
            payment_date=payment.payment_date,
            amount=payment.amount,
            payment_method=payment.payment_method
        )
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        return db_payment
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def get_payments_by_user(db: Session, user_id: int):
    try:
        return db.query(models.Payment).filter(models.Payment.user_id == user_id).all()
    except SQLAlchemyError as e:
        raise e
