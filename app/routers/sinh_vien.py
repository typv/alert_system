from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..models import models
from ..schemas import schemas
from ..services import service
from ..database import get_db

router = APIRouter(
    prefix="/api/sinh-vien",
    tags=["SinhVien"]
)

@router.post("/", response_model=schemas.SinhVienInDB, status_code=status.HTTP_201_CREATED)
def create_sinh_vien(sinh_vien: schemas.SinhVienCreate, db: Session = Depends(get_db)):
    return service.SinhVienService.create(db, sinh_vien)

@router.get("/", response_model=List[schemas.SinhVienInDB])
def read_sinh_viens(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.SinhVienService.get_all(db, skip, limit)

@router.get("/{sinh_vien_id}", response_model=schemas.SinhVienInDB)
def read_sinh_vien(sinh_vien_id: int, db: Session = Depends(get_db)):
    return service.SinhVienService.get_by_id(db, sinh_vien_id)

@router.get("/ma-sv/{ma_sv}", response_model=schemas.SinhVienInDB)
def read_sinh_vien_by_ma_sv(ma_sv: str, db: Session = Depends(get_db)):
    sinh_vien = service.SinhVienService.get_by_ma_sv(db, ma_sv)
    if not sinh_vien:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy sinh viên với mã: {ma_sv}"
        )
    return sinh_vien

@router.put("/{sinh_vien_id}", response_model=schemas.SinhVienInDB)
def update_sinh_vien(sinh_vien_id: int, sinh_vien_update: schemas.SinhVienUpdate, db: Session = Depends(get_db)):
    return service.SinhVienService.update(db, sinh_vien_id, sinh_vien_update)

@router.delete("/{sinh_vien_id}")
def delete_sinh_vien(sinh_vien_id: int, db: Session = Depends(get_db)):
    return service.SinhVienService.delete(db, sinh_vien_id)

@router.get("/diem/{sinh_vien_id}", response_model=List[schemas.DiemInDB])
def read_diem_by_sinh_vien(sinh_vien_id: int, db: Session = Depends(get_db)):

    services.SinhVienService.get_by_id(db, sinh_vien_id)
    return service.DiemService.get_by_sinhvien(db, sinh_vien_id)