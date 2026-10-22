import os


# Vercel's deployed function filesystem is read-only except for /tmp.  The
# temporary SQLite fallback keeps the portfolio demo runnable when a hosted
# database has not yet been configured.  It is intentionally ephemeral: use a
# managed PostgreSQL DATABASE_URL before storing any meaningful demo records.
_default_database = "sqlite:////tmp/matria-care-demo.db" if os.getenv("VERCEL") else "sqlite:///./matria-care-demo.db"
DATABASE_URL = os.getenv("DATABASE_URL") or _default_database
# Supabase supplies a standard PostgreSQL URL; make the installed psycopg v3
# driver explicit for SQLAlchemy.
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-development-secret-before-deploying")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))
CORS_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")]
