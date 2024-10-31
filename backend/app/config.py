import os

class Settings:
    DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://user:password@localhost:3306/satcom_db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    WEBHOOK_API_KEY = os.getenv('WEBHOOK_API_KEY', 'your-webhook-api-key')  # New Line

settings = Settings()
