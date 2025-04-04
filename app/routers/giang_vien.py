from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..models import models
from ..schemas import schemas
from ..services import service
from ..database import get_db

router = APIRouter(
    prefix="/api/giang-vien",
    tags=["GiangVien"]
)

@router.post("/", response_model=schemas.GiangVienInDB, status_code=status.HTTP_201_CREATED)
def create_giang_vien(giang_vien: schemas.GiangVienCreate, db: Session = Depends(get_db)):
    return service.GiangVienService.create(db, giang_vien)

@router.get("/", response_model=List[schemas.GiangVienInDB])
def read_giang_viens(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.GiangVienService.get_all(db, skip, limit)

@router.get("/{giang_vien_id}", response_model=schemas.GiangVienInDB)
def read_giang_vien(giang_vien_id: int, db: Session = Depends(get_db)):
    return service.GiangVienService.get_by_id(db, giang_vien_id)

@router.get("/ma-gv/{ma_gv}", response_model=schemas.GiangVienInDB)
def read_giang_vien_by_ma_gv(ma_gv: str, db: Session = Depends(get_db)):
    giang_vien = service.GiangVienService.get_by_ma_gv(db, ma_gv)
    if not giang_vien:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy giảng viên với mã: {ma_gv}"
        )
    return giang_vien

@router.put("/{giang_vien_id}", response_model=schemas.GiangVienInDB)
def update_giang_vien(giang_vien_id: int, giang_vien_update: schemas.GiangVienUpdate, db: Session = Depends(get_db)):
    return service.GiangVienService.update(db, giang_vien_id, giang_vien_update)

@router.delete("/{giang_vien_id}")
def delete_giang_vien(giang_vien_id: int, db: Session = Depends(get_db)):
    return service.GiangVienService.delete(db, giang_vien_id)

@router.get("/lop-hoc/{giang_vien_id}", response_model=List[schemas.LopHocInDB])
def read_lop_hoc_by_giang_vien(giang_vien_id: int, db: Session = Depends(get_db)):
    service.GiangVienService.get_by_id(db, giang_vien_id)
    return service.LopHocService.get_by_giangvien(db, giang_vien_id)