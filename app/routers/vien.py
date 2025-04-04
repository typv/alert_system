from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..models import models
from ..schemas import schemas
from ..services import service
from ..database import get_db

router = APIRouter(
    prefix="/api/vien",
    tags=["Vien"]
)

@router.post("/", response_model=schemas.VienInDB, status_code=status.HTTP_201_CREATED)
def create_vien(vien: schemas.VienCreate, db: Session = Depends(get_db)):
    return service.VienService.create_vien(db, vien)

@router.get("/", response_model=List[schemas.VienInDB])
def read_viens(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.VienService.get_viens(db, skip, limit)

@router.get("/{vien_id}", response_model=schemas.VienDetail)
def read_vien(vien_id: int, db: Session = Depends(get_db)):
    return service.VienService.get_vien_by_ma_vien(db, vien_id)

@router.get("/ma-vien/{ma_vien}", response_model=schemas.VienInDB)
def read_vien_by_ma_vien(ma_vien: str, db: Session = Depends(get_db)):
    vien = service.VienService.get_vien_by_ma_vien(db, ma_vien)
    if not vien:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy viên với ma_vien: {ma_vien}"
        )
    return vien

@router.put("/{vien_id}", response_model=schemas.VienInDB)
def update_vien(vien_id: int, vien_update: schemas.VienUpdate, db: Session = Depends(get_db)):
    return service.VienService.update_vien(db, vien_id, vien_update)

@router.delete("/{vien_id}")
def delete_vien(vien_id: int, db: Session = Depends(get_db)):
    return service.VienService.delete_vien(db, vien_id)