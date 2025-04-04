from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    vai_tro: Optional[str] = None

# Login Schema
class UserLogin(BaseModel):
    username: str
    password: str
    
# NguoiDung Schemas
class NguoiDungBase(BaseModel):
    ten_dang_nhap: str
    email: EmailStr
    ho_ten: str
    vai_tro: str

class NguoiDungCreate(NguoiDungBase):
    mat_khau: str

class NguoiDungUpdate(BaseModel):
    ho_ten: Optional[str] = None
    email: Optional[EmailStr] = None
    vai_tro: Optional[str] = None
    trang_thai: Optional[bool] = None

class NguoiDungInDB(NguoiDungBase):
    id: int
    trang_thai: bool

    class Config:
        orm_mode = True

# SinhVien Schemas
class SinhVienBase(BaseModel):
    ma_sv: str
    ho_ten: str
    ngay_sinh: date
    gioi_tinh: str
    dia_chi: Optional[str] = None
    so_dien_thoai: Optional[str] = None
    email: EmailStr
    nam_nhap_truong: int

class SinhVienCreate(SinhVienBase):
    nguoidung_id: Optional[int] = None

class SinhVienUpdate(BaseModel):
    ho_ten: Optional[str] = None
    ngay_sinh: Optional[date] = None
    gioi_tinh: Optional[str] = None
    dia_chi: Optional[str] = None
    so_dien_thoai: Optional[str] = None
    email: Optional[EmailStr] = None
    nam_nhap_truong: Optional[int] = None

class SinhVienInDB(SinhVienBase):
    id: int
    nguoidung_id: Optional[int] = None

    class Config:
        orm_mode = True
# GiangVien Schemas
class GiangVienBase(BaseModel):
    ma_gv: str
    hoc_vi: str
    chuyen_mon: str
    so_dien_thoai: Optional[str] = None
    vien_id: int

class GiangVienCreate(GiangVienBase):
    nguoidung_id: Optional[int] = None

class GiangVienUpdate(BaseModel):
    hoc_vi: Optional[str] = None
    chuyen_mon: Optional[str] = None
    so_dien_thoai: Optional[str] = None
    vien_id: Optional[int] = None

class GiangVienInDB(GiangVienBase):
    id: int
    nguoidung_id: Optional[int] = None

    class Config:
        orm_mode = True


# HocPhan Schemas
class HocPhanBase(BaseModel):
    ma_hp: str
    ten_hp: str
    so_tin_chi: int
    mo_ta: Optional[str] = None
    vien_id: int

class HocPhanCreate(HocPhanBase):
    pass

class HocPhanUpdate(BaseModel):
    ten_hp: Optional[str] = None
    so_tin_chi: Optional[int] = None
    mo_ta: Optional[str] = None
    vien_id: Optional[int] = None 

class HocPhanInDB(HocPhanBase):
    id: int

    class Config:
        orm_mode = True

# LopHoc Schemas
class LopHocBase(BaseModel):
    ma_lop: str
    ten_lop: str
    hocphan_id: int
    giangvien_id: int
    hoc_ky: str
    nam_hoc: str
    phong_hoc: Optional[str] = None

class LopHocCreate(LopHocBase):
    pass

class LopHocUpdate(BaseModel):
    ten_lop: Optional[str] = None
    hocphan_id: Optional[int] = None
    giangvien_id: Optional[int] = None
    hoc_ky: Optional[str] = None
    nam_hoc: Optional[str] = None
    phong_hoc: Optional[str] = None

class LopHocInDB(LopHocBase):
    id: int

    class Config:
        orm_mode = True

class LopHocDetail(LopHocInDB):
    hocphan: HocPhanInDB
    giangvien: GiangVienInDB
    
    class Config:
        orm_mode = True

# Diem Schemas
class DiemBase(BaseModel):
    sinhvien_id: int
    lophoc_id: int
    diem_chuyen_can: Optional[float] = None
    diem_giua_ky: Optional[float] = None
    diem_cuoi_ky: Optional[float] = None
    diem_tong_ket: Optional[float] = None

class DiemCreate(DiemBase):
    pass

class DiemUpdate(BaseModel):
    diem_chuyen_can: Optional[float] = None
    diem_giua_ky: Optional[float] = None
    diem_cuoi_ky: Optional[float] = None
    diem_tong_ket: Optional[float] = None

class DiemInDB(DiemBase):
    id: int

    class Config:
        orm_mode = True

class DiemDetail(DiemInDB):
    sinhvien: SinhVienInDB
    lophoc: LopHocInDB
    
    class Config:
        orm_mode = True
# Vien Schemas
class VienBase(BaseModel):
    ma_vien: str
    ten_vien: str
    mo_ta: Optional[str] = None
    nguoi_quan_ly: Optional[str] = None

class VienCreate(VienBase):
    pass

class VienUpdate(BaseModel):
    ten_vien: Optional[str] = None
    mo_ta: Optional[str] = None
    nguoi_quan_ly: Optional[str] = None

class VienInDB(VienBase):
    id: int

    class Config:
        orm_mode = True

class VienDetail(VienInDB):
    hocphan: List[HocPhanInDB] = []
    giangvien: List[GiangVienInDB] = []
    
    class Config:
        orm_mode = True

# TienDoHocTap Schemas
class TienDoHocTapBase(BaseModel):
    sinhvien_id: int
    hoc_ky: str
    nam_hoc: str
    tin_chi_dang_ky: int
    diem_trung_binh_hk: Optional[float] = None
    tong_tin_chi_tich_luy: Optional[int] = None
    diem_trung_binh_tich_luy: Optional[float] = None
    xu_ly_hoc_tap: Optional[str] = None

class TienDoHocTapCreate(TienDoHocTapBase):
    pass

class TienDoHocTapUpdate(BaseModel):
    hoc_ky: Optional[str] = None
    nam_hoc: Optional[str] = None
    tin_chi_dang_ky: Optional[int] = None
    diem_trung_binh_hk: Optional[float] = None
    tong_tin_chi_tich_luy: Optional[int] = None
    diem_trung_binh_tich_luy: Optional[float] = None
    xu_ly_hoc_tap: Optional[str] = None

class TienDoHocTapInDB(TienDoHocTapBase):
    id: int

    class Config:
        orm_mode = True

class TienDoHocTapDetail(TienDoHocTapInDB):
    sinhvien: SinhVienInDB
    
    class Config:
        orm_mode = True