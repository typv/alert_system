from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from ..database import get_db
from ..models.models import NguoiDung
from ..schemas import schemas

SECRET_KEY = "NhomBonEmLaNhomMaiAnhNgoVaThanhGayLoVaChauImANg"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def verify_password(plain_password, hashed_password):

    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):

    return pwd_context.hash(password)

def get_user_by_username(db: Session, username: str):
    return db.query(NguoiDung).filter(NguoiDung.ten_dang_nhap == username).first()

def authenticate_user(db: Session, username: str, password: str):

    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.mat_khau_hash):
        return False
    if not user.trang_thai:
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Không thể xác thực thông tin đăng nhập",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(
            username=username, 
            user_id=payload.get("user_id"), 
            vai_tro=payload.get("vai_tro")
        )
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    if not user.trang_thai:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị vô hiệu hóa",
        )
    return user

def get_current_active_user(current_user: NguoiDung = Depends(get_current_user)):

    if not current_user.trang_thai:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản không hoạt động"
        )
    return current_user

def check_user_role(required_roles: list = []):

    def check_role(current_user: NguoiDung = Depends(get_current_user)):
        if not required_roles or current_user.vai_tro in required_roles:
            return current_user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không đủ quyền truy cập"
        )
    return check_role