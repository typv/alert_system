from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..models import models
from ..schemas import schemas
from ..services import service
from ..database import get_db

router = APIRouter(
    prefix="/api/lop-hoc",
    tags=["LopHoc"]
)

@router.post("/", response_model=schemas.LopHocInDB, status_code=status.HTTP_201_CREATED)
def create_lop_hoc(lop_hoc: schemas.LopHocCreate, db: Session = Depends(get_db)):
    return service.LopHocService.create(db, lop_hoc)

@router.get("/", response_model=List[schemas.LopHocInDB])
def read_lop_hocs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.LopHocService.get_all(db, skip, limit)

@router.get("/{lop_hoc_id}", response_model=schemas.LopHocInDB)
def read_lop_hoc(lop_hoc_id: int, db: Session = Depends(get_db)):
    return service.LopHocService.get_by_id(db, lop_hoc_id)

@router.get("/detail/{lop_hoc_id}", response_model=schemas.LopHocDetail)
def read_lop_hoc_detail(lop_hoc_id: int, db: Session = Depends(get_db)):
    return service.LopHocService.get_detail_by_id(db, lop_hoc_id)

@router.get("/ma-lop/{ma_lop}", response_model=schemas.LopHocInDB)
def read_lop_hoc_by_ma_lop(ma_lop: str, db: Session = Depends(get_db)):
    lop_hoc = service.LopHocService.get_by_ma_lop(db, ma_lop)
    if not lop_hoc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy lớp học với mã: {ma_lop}"
        )
    return lop_hoc

@router.put("/{lop_hoc_id}", response_model=schemas.LopHocInDB)
def update_lop_hoc(lop_hoc_id: int, lop_hoc_update: schemas.LopHocUpdate, db: Session = Depends(get_db)):
    return service.LopHocService.update(db, lop_hoc_id, lop_hoc_update)

@router.delete("/{lop_hoc_id}")
def delete_lop_hoc(lop_hoc_id: int, db: Session = Depends(get_db)):
    return service.LopHocService.delete(db, lop_hoc_id)

@router.get("/diem/{lop_hoc_id}", response_model=List[schemas.DiemInDB])
def read_diem_by_lop_hoc(lop_hoc_id: int, db: Session = Depends(get_db)):
    service.LopHocService.get_by_id(db, lop_hoc_id)
    return service.DiemService.get_by_lophoc(db, lop_hoc_id)