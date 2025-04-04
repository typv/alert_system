from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..models import models
from ..schemas import schemas
from ..services import service
from ..database import get_db

router = APIRouter(
    prefix="/api/nguoi-dung",
    tags=["NguoiDung"]
)

@router.post("/", response_model=schemas.NguoiDungInDB, status_code=status.HTTP_201_CREATED)
def create_nguoi_dung(nguoi_dung: schemas.NguoiDungCreate, db: Session = Depends(get_db)):
    return service.NguoiDungService.create(db, nguoi_dung)

@router.get("/", response_model=List[schemas.NguoiDungInDB])
def read_nguoi_dungs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.NguoiDungService.get_all(db, skip, limit)

@router.get("/{nguoi_dung_id}", response_model=schemas.NguoiDungInDB)
def read_nguoi_dung(nguoi_dung_id: int, db: Session = Depends(get_db)):
    return service.NguoiDungService.get_by_id(db, nguoi_dung_id)

@router.get("/username/{ten_dang_nhap}", response_model=schemas.NguoiDungInDB)
def read_nguoi_dung_by_username(ten_dang_nhap: str, db: Session = Depends(get_db)):
    nguoi_dung = service.NguoiDungService.get_by_username(db, ten_dang_nhap)
    if not nguoi_dung:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy người dùng với tên đăng nhập: {ten_dang_nhap}"
        )
    return nguoi_dung

@router.get("/email/{email}", response_model=schemas.NguoiDungInDB)
def read_nguoi_dung_by_email(email: str, db: Session = Depends(get_db)):
    nguoi_dung = service.NguoiDungService.get_by_email(db, email)
    if not nguoi_dung:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy người dùng với email: {ten_dang_nhap}"
        )
    return nguoi_dung

@router.put("/{nguoi_dung_id}", response_model=schemas.NguoiDungInDB)
def update_nguoi_dung(nguoi_dung_id: int, nguoi_dung_update: schemas.NguoiDungUpdate, db: Session = Depends(get_db)):
    return service.NguoiDungService.update(db, nguoi_dung_id, nguoi_dung_update)

@router.delete("/{nguoi_dung_id}")
def delete_nguoi_dung(nguoi_dung_id: int, db: Session = Depends(get_db)):
    return service.NguoiDungService.delete(db, nguoi_dung_id)