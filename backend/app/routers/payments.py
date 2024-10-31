from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .. import schemas, models, crud, auth, database

router = APIRouter(
    prefix="/payments",
    tags=["payments"]
)

@router.get("/me", response_model=list[schemas.Payment])
def get_my_payments(current_user: schemas.User = Depends(auth.get_current_user)):
    db = database.SessionLocal()
    try:
        payments = crud.get_payments_by_user(db, user_id=current_user.user_id)
        if not payments:
            raise HTTPException(status_code=404, detail="No payments found for the user")
        return payments
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to retrieve payments")
    finally:
        db.close()

@router.get("/{user_id}", response_model=list[schemas.Payment])
def get_payments(user_id: int, db: Session = Depends(database.get_db)):
    try:
        payments = crud.get_payments_by_user(db, user_id=user_id)
        if not payments:
            raise HTTPException(status_code=404, detail="No payments found for the user")
        return payments
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to retrieve payments")
