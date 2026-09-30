from fastapi import Cookie, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from .auth import decode_access_token
from .database import get_db
from .models import User

bearer = HTTPBearer(auto_error=False)

def get_token(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), access_token: str | None = Cookie(default=None)):
    return credentials.credentials if credentials else access_token

def get_current_user(token: str | None = Depends(get_token), db: Session = Depends(get_db)):
    if not token: raise HTTPException(401, "Authentication required")
    user_id = decode_access_token(token)
    if not user_id: raise HTTPException(401, "Invalid or expired token")
    user = db.get(User, int(user_id))
    if not user: raise HTTPException(401, "User not found")
    return user
