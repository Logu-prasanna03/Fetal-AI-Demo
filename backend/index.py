"""Native Vercel FastAPI entrypoint.

Keeping the application at the project root lets Vercel forward the original
request path to FastAPI (for example, /health and /api/v1/auth/login).
"""

from app.main import app
