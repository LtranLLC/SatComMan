from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from starlette.requests import Request
from fastapi.responses import JSONResponse
from .database import engine
from . import models
from .routers import users, usage, billing, payments, webhook

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SatComMan API",
    description="API for managing users and satellite communication usage.",
    version="1.0.0"
)

# Include routers
app.include_router(users.router)
app.include_router(usage.router)
app.include_router(billing.router)
app.include_router(payments.router)
app.include_router(webhook.router)

# Custom exception handlers
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred."}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."}
    )

@app.get("/")
async def read_root():
    return {"message": "Welcome to the SatComMan API"}
