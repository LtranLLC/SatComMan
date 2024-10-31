from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Header
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .. import schemas, models, crud, database, config
from datetime import datetime

router = APIRouter(
    prefix="/webhook",
    tags=["webhook"]
)

def process_device_data(db: Session, data: schemas.DeviceDataCreate):
    """Function to process and store device data and update user usage."""
    try:
        # Check if message_id already exists to prevent duplicate processing
        existing_message = db.query(models.DeviceData).filter(models.DeviceData.message_id == data.message_id).first()
        if existing_message:
            # Message already processed
            return

        # Store the device data
        device_data = models.DeviceData(
            imei=data.imei,
            number=data.number,
            lat=data.lat,
            lng=data.lng,
            speed=data.speed,
            heading=data.heading,
            battery_status=data.battery_status,
            payload=data.payload,
            usage=data.usage,
            message_id=data.message_id,
            datetime=data.datetime,
            timestamp=datetime.utcnow()
        )
        db.add(device_data)

        # Find the user by phone number or IMEI
        user = db.query(models.User).filter(
            (models.User.phone_number == data.number) | (models.User.imei == data.imei)
        ).first()

        if user:
            # Update the user's usage
            usage_record = models.Usage(
                user_id=user.user_id,
                call_duration=0.0,  # Assuming no call duration from this message
                data_used=data.usage,
                timestamp=datetime.utcfromtimestamp(data.datetime)
            )
            db.add(usage_record)

            # For prepaid users, deduct balance
            if user.account_type == models.AccountType.Prepaid:
                cost_per_mb = 0.05  # Example cost per MB
                total_cost = data.usage * cost_per_mb
                user.balance -= total_cost
                if user.balance < 0:
                    user.account_status = models.AccountStatus.Suspended

        db.commit()
    except IntegrityError:
        db.rollback()
        # Message ID already exists, so we can safely ignore or log this occurrence
    except SQLAlchemyError as e:
        db.rollback()
        # Add logging here if needed
        raise e

@router.post("/", status_code=200)
def receive_device_data(
    data: schemas.DeviceDataCreate,
    background_tasks: BackgroundTasks,
    x_api_key: str = Header(...),  # API key from header
    db: Session = Depends(database.get_db)
):
    """Non-blocking endpoint to receive device data."""
    # Verify API key
    if x_api_key != config.settings.WEBHOOK_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    # Process data in the background
    background_tasks.add_task(process_device_data, db, data)
    return {"detail": "Data received ok"}
