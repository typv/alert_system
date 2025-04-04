from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..models import models
from ..schemas import schemas
from ..services import service
from ..database import get_db

router = APIRouter(
    prefix="/api/hoc-phan",
    tags=["HocPhan"]
)

@router.post("/", response_model=schemas.HocPhanInDB, status_code=status.HTTP_201_CREATED)
def create_hoc_phan(hoc_phan: schemas.HocPhanCreate, db: Session = Depends(get_db)):
    return service.HocPhanService.create(db, hoc_phan)

@router.get("/", response_model=List[schemas.HocPhanInDB])
def read_hoc_phans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.HocPhanService.get_all(db, skip, limit)

@router.get("/{hoc_phan_id}", response_model=schemas.HocPhanInDB)
def read_hoc_phan(hoc_phan_id: int, db: Session = Depends(get_db)):
    return service.HocPhanService.get_by_id(db, hoc_phan_id)

@router.get("/ma-hp/{ma_hp}", response_model=schemas.HocPhanInDB)
def read_hoc_phan_by_ma_hp(ma_hp: str, db: Session = Depends(get_db)):
    hoc_phan = service.HocPhanService.get_by_ma_hp(db, ma_hp)
    if not hoc_phan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy học phần với mã: {ma_hp}"
        )
    return hoc_phan

@router.put("/{hoc_phan_id}", response_model=schemas.HocPhanInDB)
def update_hoc_phan(hoc_phan_id: int, hoc_phan_update: schemas.HocPhanUpdate, db: Session = Depends(get_db)):
    return service.HocPhanService.update(db, hoc_phan_id, hoc_phan_update)

@router.delete("/{hoc_phan_id}")
def delete_hoc_phan(hoc_phan_id: int, db: Session = Depends(get_db)):
    return service.HocPhanService.delete(db, hoc_phan_id)

@router.get("/lop-hoc/{hoc_phan_id}", response_model=List[schemas.LopHocInDB])
def read_lop_hoc_by_hoc_phan(hoc_phan_id: int, db: Session = Depends(get_db)):
    service.HocPhanService.get_by_id(db, hoc_phan_id)
    return service.LopHocService.get_by_hocphan(db, hoc_phan_id)