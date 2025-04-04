from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.models import NguoiDung, SinhVien, GiangVien
from ..schemas.schemas import NguoiDungCreate, Token, UserLogin
from ..services.auth_service import (
    authenticate_user, 
    create_access_token, 
    get_password_hash, 
    get_current_user,
    check_user_role,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(
    prefix="/xacthuc",
    tags=["authentication"],
    responses={401: {"description": "Unauthorized"}},
)

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.ten_dang_nhap, 
            "user_id": user.id, 
            "vai_tro": user.vai_tro
        },
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.ten_dang_nhap, 
            "user_id": user.id, 
            "vai_tro": user.vai_tro
        },
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: NguoiDungCreate,
    db: Session = Depends(get_db)
):

    db_user = db.query(NguoiDung).filter(NguoiDung.ten_dang_nhap == user_data.ten_dang_nhap).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên đăng nhập đã tồn tại"
        )
    
    db_email = db.query(NguoiDung).filter(NguoiDung.email == user_data.email).first()
    if db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã được sử dụng"
        )
    
    hashed_password = get_password_hash(user_data.mat_khau)
    new_user = NguoiDung(
        ten_dang_nhap=user_data.ten_dang_nhap,
        email=user_data.email,
        ho_ten=user_data.ho_ten,
        vai_tro=user_data.vai_tro,
        mat_khau_hash=hashed_password,
        trang_thai=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "Đăng ký tài khoản thành công"}

@router.get("/me")
async def read_users_me(current_user: NguoiDung = Depends(get_current_user)):

    user_info = {
        "id": current_user.id,
        "ten_dang_nhap": current_user.ten_dang_nhap,
        "email": current_user.email,
        "ho_ten": current_user.ho_ten,
        "vai_tro": current_user.vai_tro,
        "trang_thai": current_user.trang_thai
    }
    
    if current_user.vai_tro == "sinh_vien":
        sinh_vien = db.query(SinhVien).filter(SinhVien.nguoidung_id == current_user.id).first()
        if sinh_vien:
            user_info["sinh_vien"] = {
                "id": sinh_vien.id,
                "ma_sv": sinh_vien.ma_sv,
                "ngay_sinh": sinh_vien.ngay_sinh,
                "gioi_tinh": sinh_vien.gioi_tinh,
                "dia_chi": sinh_vien.dia_chi,
                "so_dien_thoai": sinh_vien.so_dien_thoai
            }
    elif current_user.vai_tro == "giang_vien":
        giang_vien = db.query(GiangVien).filter(GiangVien.nguoidung_id == current_user.id).first()
        if giang_vien:
            user_info["giang_vien"] = {
                "id": giang_vien.id,
                "ma_gv": giang_vien.ma_gv,
                "hoc_vi": giang_vien.hoc_vi,
                "chuyen_mon": giang_vien.chuyen_mon,
                "so_dien_thoai": giang_vien.so_dien_thoai
            }
    
    return user_info

@router.get("/admin-only")
async def admin_route(current_user: NguoiDung = Depends(check_user_role(["admin"]))):
    """Route chỉ dành cho admin"""
    return {"message": "Bạn có quyền truy cập vào khu vực admin"}

@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    old_password: str,
    new_password: str,
    current_user: NguoiDung = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if not verify_password(old_password, current_user.mat_khau):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mật khẩu cũ không chính xác"
        )
    
    current_user.mat_khau = get_password_hash(new_password)
    db.commit()
    
    return {"message": "Đổi mật khẩu thành công"}