import os


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fetalai.db")
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-development-secret-before-deploying")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))
CORS_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")]
