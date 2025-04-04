from enum import Enum
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date, Table, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from ..database import Base

lophoc_sinhvien = Table('lophoc_sinhvien', Base.metadata,
    Column('lophoc_id', Integer, ForeignKey('lophoc.id'), primary_key=True),
    Column('sinhvien_id', Integer, ForeignKey('sinhvien.id'), primary_key=True)
)

class Vien(Base):
    __tablename__ = "vien"

    id = Column(Integer, primary_key=True, index=True)
    ma_vien = Column(String, unique=True, index=True)
    ten_vien = Column(String)
    mo_ta = Column(String)
    nguoi_quan_ly = Column(String)
    
    hocphan = relationship("HocPhan", back_populates="vien")
    giangvien = relationship("GiangVien", back_populates="vien")

class NguoiDung(Base):
    __tablename__ = "nguoidung"

    id = Column(Integer, primary_key=True, index=True)
    ten_dang_nhap = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    mat_khau_hash = Column(String)
    ho_ten = Column(String)
    vai_tro = Column(String)  # 'admin', 'giangvien', 'sinhvien'
    trang_thai = Column(Boolean, default=True)

    sinhvien = relationship("SinhVien", back_populates="nguoidung", uselist=False)
    giangvien = relationship("GiangVien", back_populates="nguoidung", uselist=False)


class SinhVien(Base):
    __tablename__ = "sinhvien"

    id = Column(Integer, primary_key=True, index=True)
    ma_sv = Column(String, unique=True, index=True)
    ho_ten = Column(String)
    ngay_sinh = Column(Date)
    gioi_tinh = Column(String)
    dia_chi = Column(String)
    so_dien_thoai = Column(String)
    email = Column(String, unique=True)
    nam_nhap_truong = Column(Integer)
    nguoidung_id = Column(Integer, ForeignKey("nguoidung.id"))
    
    nguoidung = relationship("NguoiDung", back_populates="sinhvien")
    diem = relationship("Diem", back_populates="sinhvien")
    lophoc = relationship("LopHoc", secondary=lophoc_sinhvien, back_populates="sinhvien")
    tiendohoctap = relationship("TienDoHocTap", back_populates="sinhvien")


class GiangVien(Base):
    __tablename__ = "giangvien"

    id = Column(Integer, primary_key=True, index=True)
    ma_gv = Column(String, unique=True, index=True)
    ho_ten = Column(String)
    hoc_vi = Column(String)
    chuyen_mon = Column(String)
    so_dien_thoai = Column(String)
    email = Column(String, unique=True)
    nguoidung_id = Column(Integer, ForeignKey("nguoidung.id"))
    vien_id = Column(Integer, ForeignKey("vien.id"))
    
    nguoidung = relationship("NguoiDung", back_populates="giangvien")
    lophoc = relationship("LopHoc", back_populates="giangvien")
    vien = relationship("Vien", back_populates="giangvien")
class LoaiHocPhan(str, Enum): 
    DAICUONG = "DAICUONG"
    COSONGANH = "COSONGANH"
    CHUYENNGANH = "CHUYENNGANH"

class HocPhan(Base):
    __tablename__ = "hocphan"

    id = Column(Integer, primary_key=True, index=True)
    ma_hp = Column(String, unique=True, index=True)
    ten_hp = Column(String)
    so_tin_chi = Column(Integer)
    mo_ta = Column(String)
    vien_id = Column(Integer, ForeignKey("vien.id"))
    loai_hoc_phan = Column(SQLAlchemyEnum(LoaiHocPhan), nullable=False)
    
    vien = relationship("Vien", back_populates="hocphan")
    lophoc = relationship("LopHoc", back_populates="hocphan")


class LopHoc(Base):
    __tablename__ = "lophoc"

    id = Column(Integer, primary_key=True, index=True)
    ma_lop = Column(String, unique=True, index=True)
    ten_lop = Column(String)
    hocphan_id = Column(Integer, ForeignKey("hocphan.id"))
    giangvien_id = Column(Integer, ForeignKey("giangvien.id"))
    hoc_ky = Column(String)
    nam_hoc = Column(String)
    phong_hoc = Column(String)
    
    hocphan = relationship("HocPhan", back_populates="lophoc")
    giangvien = relationship("GiangVien", back_populates="lophoc")
    sinhvien = relationship("SinhVien", secondary=lophoc_sinhvien, back_populates="lophoc")
    diem = relationship("Diem", back_populates="lophoc")


class Diem(Base):
    __tablename__ = "diem"

    id = Column(Integer, primary_key=True, index=True)
    sinhvien_id = Column(Integer, ForeignKey("sinhvien.id"))
    lophoc_id = Column(Integer, ForeignKey("lophoc.id"))
    diem_chuyen_can = Column(Float)
    diem_giua_ky = Column(Float)
    diem_cuoi_ky = Column(Float)
    diem_tong_ket = Column(Float)
    
    sinhvien = relationship("SinhVien", back_populates="diem")
    lophoc = relationship("LopHoc", back_populates="diem")


class TienDoHocTap(Base):
    __tablename__ = "tiendohoctap"

    id = Column(Integer, primary_key=True, index=True)
    sinhvien_id = Column(Integer, ForeignKey("sinhvien.id"))
    hoc_ky = Column(String)  
    nam_hoc = Column(String)  
    tin_chi_dang_ky = Column(Integer)  
    diem_trung_binh_hk = Column(Float)  
    tong_tin_chi_tich_luy = Column(Integer) 
    diem_trung_binh_tich_luy = Column(Float)  
    xu_ly_hoc_tap = Column(String) 
    
    sinhvien = relationship("SinhVien", back_populates="tiendohoctap")