from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .. import schemas, models, crud, auth, database

router = APIRouter(
    prefix="/usage",
    tags=["usage"]
)

@router.post("/", response_model=schemas.Usage)
def add_usage(usage: schemas.UsageCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=usage.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        return crud.add_usage(db=db, usage=usage)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to add usage record")

@router.get("/me", response_model=list[schemas.Usage])
def get_my_usage(current_user: schemas.User = Depends(auth.get_current_user)):
    db = database.SessionLocal()
    try:
        usage_records = crud.get_usage_by_user(db, user_id=current_user.user_id)
        if not usage_records:
            raise HTTPException(status_code=404, detail="No usage records found for the user")
        return usage_records
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to retrieve usage records")
    finally:
        db.close()

@router.get("/{user_id}", response_model=list[schemas.Usage])
def get_usage(user_id: int, db: Session = Depends(database.get_db)):
    try:
        usage_records = crud.get_usage_by_user(db, user_id=user_id)
        if not usage_records:
            raise HTTPException(status_code=404, detail="No usage records found for the user")
        return usage_records
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to retrieve usage records")

