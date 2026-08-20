from datetime import UTC, datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from app.core.database import get_db
from app.models import User

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(user: User) -> str:
    expires = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": str(user.id), "role": user.role, "exp": expires}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session")
    try:
        user_id = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if not user_id:
            raise credentials_error
    except JWTError as error:
        raise credentials_error from error
    user = db.get(User, int(user_id))
    if not user:
        raise credentials_error
    return user


def require_role(role: str):
    def check(user: User = Depends(get_current_user)) -> User:
        if user.role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this area")
        return user
    return check
