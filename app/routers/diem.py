from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import models
from ..schemas import schemas
from ..services import service
from ..database import get_db

router = APIRouter(
    prefix="/api/diem",
    tags=["Diem"]
)

@router.post("/", response_model=schemas.DiemInDB, status_code=status.HTTP_201_CREATED)
def create_diem(diem: schemas.DiemCreate, db: Session = Depends(get_db)):
    return services.DiemService.create(db, diem)

@router.get("/", response_model=List[schemas.DiemInDB])
def read_diems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.DiemService.get_all(db, skip, limit)

@router.get("/{diem_id}", response_model=schemas.DiemInDB)
def read_diem(diem_id: int, db: Session = Depends(get_db)):
    return services.DiemService.get_by_id(db, diem_id)

@router.get("/detail/{diem_id}", response_model=schemas.DiemDetail)
def read_diem_detail(diem_id: int, db: Session = Depends(get_db)):
    return services.DiemService.get_detail_by_id(db, diem_id)

@router.get("/sinh-vien/{sinhvien_id}/lop-hoc/{lophoc_id}", response_model=schemas.DiemInDB)
def read_diem_by_sinhvien_lophoc(sinhvien_id: int, lophoc_id: int, db: Session = Depends(get_db)):
    return services.DiemService.get_by_sinhvien_lophoc(db, sinhvien_id, lophoc_id)

@router.put("/{diem_id}", response_model=schemas.DiemInDB)
def update_diem(diem_id: int, diem_update: schemas.DiemUpdate, db: Session = Depends(get_db)):
    return services.DiemService.update(db, diem_id, diem_update)

@router.put("/sinh-vien/{sinhvien_id}/lop-hoc/{lophoc_id}", response_model=schemas.DiemInDB)
def update_diem_by_sinhvien_lophoc(
    sinhvien_id: int, 
    lophoc_id: int, 
    diem_update: schemas.DiemUpdate, 
    db: Session = Depends(get_db)
):
    return services.DiemService.update_by_sinhvien_lophoc(db, sinhvien_id, lophoc_id, diem_update)

@router.delete("/{diem_id}")
def delete_diem(diem_id: int, db: Session = Depends(get_db)):
    return services.DiemService.delete(db, diem_id)

@router.delete("/sinh-vien/{sinhvien_id}/lop-hoc/{lophoc_id}")
def delete_diem_by_sinhvien_lophoc(sinhvien_id: int, lophoc_id: int, db: Session = Depends(get_db)):
    return services.DiemService.delete_by_sinhvien_lophoc(db, sinhvien_id, lophoc_id)