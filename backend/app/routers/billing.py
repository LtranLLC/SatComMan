from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .. import schemas, models, crud, auth, database

router = APIRouter(
    prefix="/billing",
    tags=["billing"]
)

@router.post("/generate/{user_id}", response_model=schemas.Billing)
def generate_bill(user_id: int, billing: schemas.BillingCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        return crud.create_billing(db=db, billing=billing)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to generate bill")

@router.get("/me", response_model=list[schemas.Billing])
def get_my_billing(current_user: schemas.User = Depends(auth.get_current_user)):
    db = database.SessionLocal()
    try:
        billing_records = crud.get_billing_by_user(db, user_id=current_user.user_id)
        if not billing_records:
            raise HTTPException(status_code=404, detail="No billing records found for the user")
        return billing_records
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to retrieve billing records")
    finally:
        db.close()

@router.get("/{user_id}", response_model=list[schemas.Billing])
def get_billing(user_id: int, db: Session = Depends(database.get_db)):
    try:
        billing_records = crud.get_billing_by_user(db, user_id=user_id)
        if not billing_records:
            raise HTTPException(status_code=404, detail="No billing records found for the user")
        return billing_records
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to retrieve billing records")

@router.post("/pay/{user_id}", response_model=schemas.Payment)
def make_payment(user_id: int, payment: schemas.PaymentCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        return crud.make_payment(db=db, payment=payment)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to process payment")
