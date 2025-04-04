from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import (
    learning_result,
    diem,
    giang_vien,
    hoc_phan,
    lop_hoc,
    nguoi_dung,
    sinh_vien,
    xac_thuc,
    vien
    
)
from .database import engine, Base
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="WMS API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(learning_result.router)
app.include_router(diem.router)
app.include_router(giang_vien.router)
app.include_router(hoc_phan.router)
app.include_router(lop_hoc.router)
app.include_router(nguoi_dung.router)
app.include_router(sinh_vien.router)
app.include_router(xac_thuc.router)
app.include_router(vien.router)