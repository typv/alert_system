from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import date
import bcrypt

from ..models import models
from ..schemas import schemas

class NguoiDungService:
    @staticmethod
    def create(db: Session, nguoi_dung: schemas.NguoiDungCreate):
        hashed_password = bcrypt.hashpw(nguoi_dung.mat_khau.encode('utf-8'), bcrypt.gensalt())
        
        db_nguoi_dung = models.NguoiDung(
            ten_dang_nhap=nguoi_dung.ten_dang_nhap,
            email=nguoi_dung.email,
            ho_ten=nguoi_dung.ho_ten,
            vai_tro=nguoi_dung.vai_tro,
            mat_khau_hash=hashed_password.decode('utf-8'),
            trang_thai=True
        )
        
        try:
            db.add(db_nguoi_dung)
            db.commit()
            db.refresh(db_nguoi_dung)
            return db_nguoi_dung
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tên đăng nhập hoặc email đã tồn tại trong hệ thống"
            )
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.NguoiDung).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, nguoi_dung_id: int):
        db_nguoi_dung = db.query(models.NguoiDung).filter(models.NguoiDung.id == nguoi_dung_id).first()
        if db_nguoi_dung is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy người dùng với ID: {nguoi_dung_id}"
            )
        return db_nguoi_dung
    
    @staticmethod
    def get_by_username(db: Session, ten_dang_nhap: str):
        return db.query(models.NguoiDung).filter(models.NguoiDung.ten_dang_nhap == ten_dang_nhap).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(models.NguoiDung).filter(models.NguoiDung.email == email).first()
    @staticmethod
    def search_by_email_linh_dong(db: Session, email: str) -> List[models.NguoiDung]:

        try:
            users = db.query(models.NguoiDung).filter(models.NguoiDung.email.ilike(f"%{email}%")).all()
            return users
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    @staticmethod
    def update(db: Session, nguoi_dung_id: int, nguoi_dung_update: schemas.NguoiDungUpdate):
        db_nguoi_dung = NguoiDungService.get_by_id(db, nguoi_dung_id)
        
        update_data = nguoi_dung_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_nguoi_dung, key, value)
            
        try:
            db.commit()
            db.refresh(db_nguoi_dung)
            return db_nguoi_dung
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email đã tồn tại trong hệ thống"
            )
    
    @staticmethod
    def delete(db: Session, nguoi_dung_id: int):
        db_nguoi_dung = NguoiDungService.get_by_id(db, nguoi_dung_id)
        
        db_nguoi_dung.trang_thai = False
        db.commit()
        
        return {"detail": f"Người dùng với ID {nguoi_dung_id} đã bị vô hiệu hóa"}


class SinhVienService:
    @staticmethod
    def create(db: Session, sinh_vien: schemas.SinhVienCreate):
        db_sinh_vien = models.SinhVien(
            ma_sv=sinh_vien.ma_sv,
            ho_ten=sinh_vien.ho_ten,
            ngay_sinh=sinh_vien.ngay_sinh,
            gioi_tinh=sinh_vien.gioi_tinh,
            dia_chi=sinh_vien.dia_chi,
            so_dien_thoai=sinh_vien.so_dien_thoai,
            email=sinh_vien.email,
            nguoidung_id=sinh_vien.nguoidung_id,
            nam_nhap_truong=sinh_vien.nam_nhap_truong
        )
        
        try:
            db.add(db_sinh_vien)
            db.commit()
            db.refresh(db_sinh_vien)
            return db_sinh_vien
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mã sinh viên hoặc email đã tồn tại trong hệ thống"
            )
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.SinhVien).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, sinh_vien_id: int):
        db_sinh_vien = db.query(models.SinhVien).filter(models.SinhVien.id == sinh_vien_id).first()
        if db_sinh_vien is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy sinh viên với ID: {sinh_vien_id}"
            )
        return db_sinh_vien
    
    @staticmethod
    def get_by_ma_sv(db: Session, ma_sv: str):
        return db.query(models.SinhVien).filter(models.SinhVien.ma_sv == ma_sv).first()
    
    @staticmethod
    def update(db: Session, sinh_vien_id: int, sinh_vien_update: schemas.SinhVienUpdate):
        db_sinh_vien = SinhVienService.get_by_id(db, sinh_vien_id)
        
        update_data = sinh_vien_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_sinh_vien, key, value)
            
        try:
            db.commit()
            db.refresh(db_sinh_vien)
            return db_sinh_vien
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email đã tồn tại trong hệ thống"
            )
    
    @staticmethod
    def delete(db: Session, sinh_vien_id: int):
        db_sinh_vien = SinhVienService.get_by_id(db, sinh_vien_id)
        
        db.delete(db_sinh_vien)
        db.commit()
        
        return {"detail": f"Sinh viên với ID {sinh_vien_id} đã bị xóa"}

class GiangVienService:
    @staticmethod
    def create(db: Session, giang_vien: schemas.GiangVienCreate):
        db_giang_vien = models.GiangVien(
            ma_gv=giang_vien.ma_gv,
            hoc_vi=giang_vien.hoc_vi,
            chuyen_mon=giang_vien.chuyen_mon,
            so_dien_thoai=giang_vien.so_dien_thoai,
            nguoidung_id=giang_vien.nguoidung_id,
            vien_id=giang_vien.vien_id
        )
        
        try:
            db.add(db_giang_vien)
            db.commit()
            db.refresh(db_giang_vien)
            return db_giang_vien
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mã giảng viên đã tồn tại trong hệ thống"
            )
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.GiangVien).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, giang_vien_id: int):
        db_giang_vien = db.query(models.GiangVien).filter(models.GiangVien.id == giang_vien_id).first()
        if db_giang_vien is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy giảng viên với ID: {giang_vien_id}"
            )
        return db_giang_vien
    
    @staticmethod
    def get_by_ma_gv(db: Session, ma_gv: str):
        return db.query(models.GiangVien).filter(models.GiangVien.ma_gv == ma_gv).first()
    
    @staticmethod
    def update(db: Session, giang_vien_id: int, giang_vien_update: schemas.GiangVienUpdate):
        db_giang_vien = GiangVienService.get_by_id(db, giang_vien_id)
        
        update_data = giang_vien_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_giang_vien, key, value)
            
        try:
            db.commit()
            db.refresh(db_giang_vien)
            return db_giang_vien
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lỗi khi cập nhật giảng viên"
            )
    
    @staticmethod
    def delete(db: Session, giang_vien_id: int):
        db_giang_vien = GiangVienService.get_by_id(db, giang_vien_id)
        
        db.delete(db_giang_vien)
        db.commit()
        
        return {"detail": f"Giảng viên với ID {giang_vien_id} đã bị xóa"}

class HocPhanService:
    @staticmethod
    def create(db: Session, hoc_phan: schemas.HocPhanCreate):
        db_hoc_phan = models.HocPhan(
            ma_hp=hoc_phan.ma_hp,
            ten_hp=hoc_phan.ten_hp,
            so_tin_chi=hoc_phan.so_tin_chi,
            mo_ta=hoc_phan.mo_ta,
            vien_id=hoc_phan.vien_id
        )
        
        try:
            db.add(db_hoc_phan)
            db.commit()
            db.refresh(db_hoc_phan)
            return db_hoc_phan
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mã học phần đã tồn tại trong hệ thống"
            )
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.HocPhan).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, hoc_phan_id: int):
        db_hoc_phan = db.query(models.HocPhan).filter(models.HocPhan.id == hoc_phan_id).first()
        if db_hoc_phan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy học phần với ID: {hoc_phan_id}"
            )
        return db_hoc_phan
    
    @staticmethod
    def get_by_ma_hp(db: Session, ma_hp: str):
        return db.query(models.HocPhan).filter(models.HocPhan.ma_hp == ma_hp).first()
    
    @staticmethod
    def update(db: Session, hoc_phan_id: int, hoc_phan_update: schemas.HocPhanUpdate):
        db_hoc_phan = HocPhanService.get_by_id(db, hoc_phan_id)
        
        update_data = hoc_phan_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_hoc_phan, key, value)
            
        db.commit()
        db.refresh(db_hoc_phan)
        return db_hoc_phan
    
    @staticmethod
    def delete(db: Session, hoc_phan_id: int):
        db_hoc_phan = HocPhanService.get_by_id(db, hoc_phan_id)
        
        db.delete(db_hoc_phan)
        db.commit()
        
        return {"detail": f"Học phần với ID {hoc_phan_id} đã bị xóa"}


class LopHocService:
    @staticmethod
    def create(db: Session, lop_hoc: schemas.LopHocCreate):
        HocPhanService.get_by_id(db, lop_hoc.hocphan_id)
        GiangVienService.get_by_id(db, lop_hoc.giangvien_id)
        
        db_lop_hoc = models.LopHoc(
            ma_lop=lop_hoc.ma_lop,
            ten_lop=lop_hoc.ten_lop,
            hocphan_id=lop_hoc.hocphan_id,
            giangvien_id=lop_hoc.giangvien_id,
            hoc_ky=lop_hoc.hoc_ky,
            nam_hoc=lop_hoc.nam_hoc,
            phong_hoc=lop_hoc.phong_hoc
        )
        
        try:
            db.add(db_lop_hoc)
            db.commit()
            db.refresh(db_lop_hoc)
            return db_lop_hoc
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mã lớp đã tồn tại trong hệ thống"
            )
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.LopHoc).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, lop_hoc_id: int):
        db_lop_hoc = db.query(models.LopHoc).filter(models.LopHoc.id == lop_hoc_id).first()
        if db_lop_hoc is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy lớp học với ID: {lop_hoc_id}"
            )
        return db_lop_hoc
    
    @staticmethod
    def get_detail_by_id(db: Session, lop_hoc_id: int):
        db_lop_hoc = db.query(models.LopHoc).filter(models.LopHoc.id == lop_hoc_id).first()
        if db_lop_hoc is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy lớp học với ID: {lop_hoc_id}"
            )
        return db_lop_hoc
    
    @staticmethod
    def get_by_ma_lop(db: Session, ma_lop: str):
        return db.query(models.LopHoc).filter(models.LopHoc.ma_lop == ma_lop).first()
    
    @staticmethod
    def get_by_giangvien(db: Session, giangvien_id: int):
        return db.query(models.LopHoc).filter(models.LopHoc.giangvien_id == giangvien_id).all()
    
    @staticmethod
    def get_by_hocphan(db: Session, hocphan_id: int):
        return db.query(models.LopHoc).filter(models.LopHoc.hocphan_id == hocphan_id).all()
    
    @staticmethod
    def update(db: Session, lop_hoc_id: int, lop_hoc_update: schemas.LopHocUpdate):
        db_lop_hoc = LopHocService.get_by_id(db, lop_hoc_id)
        
        update_data = lop_hoc_update.dict(exclude_unset=True)
        
        if 'hocphan_id' in update_data:
            HocPhanService.get_by_id(db, update_data['hocphan_id'])
            
        if 'giangvien_id' in update_data:
            GiangVienService.get_by_id(db, update_data['giangvien_id'])
        
        for key, value in update_data.items():
            setattr(db_lop_hoc, key, value)
            
        db.commit()
        db.refresh(db_lop_hoc)
        return db_lop_hoc
    
    @staticmethod
    def delete(db: Session, lop_hoc_id: int):
        db_lop_hoc = LopHocService.get_by_id(db, lop_hoc_id)
        
        db.delete(db_lop_hoc)
        db.commit()
        
        return {"detail": f"Lớp học với ID {lop_hoc_id} đã bị xóa"}


class DiemService:
    @staticmethod
    def create(db: Session, diem: schemas.DiemCreate):
 
        SinhVienService.get_by_id(db, diem.sinhvien_id)
        LopHocService.get_by_id(db, diem.lophoc_id)
        
        existing = db.query(models.Diem).filter(
            models.Diem.sinhvien_id == diem.sinhvien_id,
            models.Diem.lophoc_id == diem.lophoc_id
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Sinh viên đã có điểm trong lớp học này"
            )
        
        db_diem = models.Diem(
            sinhvien_id=diem.sinhvien_id,
            lophoc_id=diem.lophoc_id,
            diem_chuyen_can=diem.diem_chuyen_can,
            diem_giua_ky=diem.diem_giua_ky,
            diem_cuoi_ky=diem.diem_cuoi_ky,
            diem_tong_ket=diem.diem_tong_ket
        )
        
        db.add(db_diem)
        db.commit()
        db.refresh(db_diem)
        return db_diem
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Diem).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, diem_id: int):
        db_diem = db.query(models.Diem).filter(models.Diem.id == diem_id).first()
        if db_diem is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy điểm với ID: {diem_id}"
            )
        return db_diem
    
    @staticmethod
    def get_detail_by_id(db: Session, diem_id: int):
        db_diem = db.query(models.Diem).filter(models.Diem.id == diem_id).first()
        if db_diem is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy điểm với ID: {diem_id}"
            )
        return db_diem
    
    @staticmethod
    def get_by_sinhvien(db: Session, sinhvien_id: int):
        return db.query(models.Diem).filter(models.Diem.sinhvien_id == sinhvien_id).all()
    
    @staticmethod
    def get_by_lophoc(db: Session, lophoc_id: int):
        return db.query(models.Diem).filter(models.Diem.lophoc_id == lophoc_id).all()
    
    @staticmethod
    def get_by_sinhvien_lophoc(db: Session, sinhvien_id: int, lophoc_id: int):
        db_diem = db.query(models.Diem).filter(
            models.Diem.sinhvien_id == sinhvien_id,
            models.Diem.lophoc_id == lophoc_id
        ).first()
        
        if db_diem is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy điểm của sinh viên {sinhvien_id} trong lớp học {lophoc_id}"
            )
        return db_diem
    
    @staticmethod
    def update(db: Session, diem_id: int, diem_update: schemas.DiemUpdate):
        db_diem = DiemService.get_by_id(db, diem_id)
        
        update_data = diem_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_diem, key, value)
            
        db.commit()
        db.refresh(db_diem)
        return db_diem
    
    @staticmethod
    def update_by_sinhvien_lophoc(db: Session, sinhvien_id: int, lophoc_id: int, diem_update: schemas.DiemUpdate):
        db_diem = DiemService.get_by_sinhvien_lophoc(db, sinhvien_id, lophoc_id)
        
        update_data = diem_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_diem, key, value)
            
        db.commit()
        db.refresh(db_diem)
        return db_diem
    
    @staticmethod
    def delete(db: Session, diem_id: int):
        db_diem = DiemService.get_by_id(db, diem_id)
        
        db.delete(db_diem)
        db.commit()
        
        return {"detail": f"Điểm với ID {diem_id} đã bị xóa"}
    
    @staticmethod
    def delete_by_sinhvien_lophoc(db: Session, sinhvien_id: int, lophoc_id: int):
        db_diem = DiemService.get_by_sinhvien_lophoc(db, sinhvien_id, lophoc_id)
        
        db.delete(db_diem)
        db.commit()
        
        return {"detail": f"Điểm của sinh viên {sinhvien_id} trong lớp học {lophoc_id} đã bị xóa"}
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import date
import bcrypt

from ..models import models
from ..schemas import schemas

class VienService:
    @staticmethod
    def get_vien(db: Session, vien_id: int) -> models.Vien:
        vien = db.query(models.Vien).filter(models.Vien.id == vien_id).first()
        if vien is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Viện với ID {vien_id} không tồn tại"
            )
        return vien

    @staticmethod
    def get_vien_by_ma_vien(db: Session, ma_vien: str) -> models.Vien:
        vien = db.query(models.Vien).filter(models.Vien.ma_vien == ma_vien).first()
        if vien is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Viện với mã {ma_vien} không tồn tại"
            )
        return vien

    @staticmethod
    def get_viens(db: Session, skip: int = 0, limit: int = 100) -> List[models.Vien]:
        return db.query(models.Vien).offset(skip).limit(limit).all()

    @staticmethod
    def create_vien(db: Session, vien: schemas.VienCreate) -> models.Vien:
        try:
            db_vien = models.Vien(
                ma_vien=vien.ma_vien,
                ten_vien=vien.ten_vien,
                mo_ta=vien.mo_ta,
                nguoi_quan_ly=vien.nguoi_quan_ly
            )
            db.add(db_vien)
            db.commit()
            db.refresh(db_vien)
            return db_vien
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mã viện đã tồn tại"
            )

    @staticmethod
    def update_vien(db: Session, vien_id: int, vien: schemas.VienUpdate) -> models.Vien:
        db_vien = VienService.get_vien(db, vien_id)
        
        vien_data = vien.dict(exclude_unset=True)
        for key, value in vien_data.items():
            setattr(db_vien, key, value)
            
        try:
            db.commit()
            db.refresh(db_vien)
            return db_vien
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lỗi khi cập nhật viện, hãy kiểm tra xem mã viện có bị trùng không"
            )

    @staticmethod
    def delete_vien(db: Session, vien_id: int) -> models.Vien:
        db_vien = VienService.get_vien(db, vien_id)
        
        hoc_phans = db.query(models.HocPhan).filter(models.HocPhan.vien_id == vien_id).count()
        giang_viens = db.query(models.GiangVien).filter(models.GiangVien.vien_id == vien_id).count()
        
        if hoc_phans > 0 or giang_viens > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Không thể xóa viện này vì đang có học phần hoặc giảng viên liên kết"
            )
        
        db.delete(db_vien)
        db.commit()
        return db_vien

    @staticmethod
    def get_vien_detail(db: Session, vien_id: int) -> models.Vien:
        vien = db.query(models.Vien).filter(models.Vien.id == vien_id).first()
        if vien is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Viện với ID {vien_id} không tồn tại"
            )
        return vien


class TiendohoctapService:
    @staticmethod
    def get_tiendohoctap(db: Session, tiendohoctap_id: int) -> models.TienDoHocTap:
        tiendohoctap = db.query(models.TienDoHocTap).filter(models.TienDoHocTap.id == tiendohoctap_id).first()
        if tiendohoctap is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tiến độ học tập với ID {tiendohoctap_id} không tồn tại"
            )
        return tiendohoctap

    @staticmethod
    def get_tiendohoctaps(db: Session, skip: int = 0, limit: int = 100) -> List[models.TienDoHocTap]:
        return db.query(models.TienDoHocTap).offset(skip).limit(limit).all()

    @staticmethod
    def get_tiendohoctaps_by_sinhvien(db: Session, sinhvien_id: int) -> List[models.TienDoHocTap]:
        return db.query(models.TienDoHocTap).filter(models.TienDoHocTap.sinhvien_id == sinhvien_id).all()

    @staticmethod
    def get_tiendohoctap_by_sinhvien_hocky_namhoc(
        db: Session, sinhvien_id: int, hoc_ky: str, nam_hoc: str
    ) -> models.TienDoHocTap:
        tiendohoctap = db.query(models.TienDoHocTap).filter(
            models.TienDoHocTap.sinhvien_id == sinhvien_id,
            models.TienDoHocTap.hoc_ky == hoc_ky,
            models.TienDoHocTap.nam_hoc == nam_hoc
        ).first()
        
        if tiendohoctap is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy tiến độ học tập của sinh viên {sinhvien_id} trong học kỳ {hoc_ky} năm học {nam_hoc}"
            )
        return tiendohoctap

    @staticmethod
    def create_tiendohoctap(db: Session, tiendohoctap: schemas.TienDoHocTapCreate) -> models.TienDoHocTap:
        sinhvien = db.query(models.SinhVien).filter(models.SinhVien.id == tiendohoctap.sinhvien_id).first()
        if sinhvien is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sinh viên với ID {tiendohoctap.sinhvien_id} không tồn tại"
            )
            
        existing = db.query(models.TienDoHocTap).filter(
            models.TienDoHocTap.sinhvien_id == tiendohoctap.sinhvien_id,
            models.TienDoHocTap.hoc_ky == tiendohoctap.hoc_ky,
            models.TienDoHocTap.nam_hoc == tiendohoctap.nam_hoc
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tiến độ học tập của sinh viên {tiendohoctap.sinhvien_id} trong học kỳ {tiendohoctap.hoc_ky} năm học {tiendohoctap.nam_hoc} đã tồn tại"
            )
        
        try:
            db_tiendohoctap = models.TienDoHocTap(
                sinhvien_id=tiendohoctap.sinhvien_id,
                hoc_ky=tiendohoctap.hoc_ky,
                nam_hoc=tiendohoctap.nam_hoc,
                tin_chi_dang_ky=tiendohoctap.tin_chi_dang_ky,
                diem_trung_binh_hk=tiendohoctap.diem_trung_binh_hk,
                tong_tin_chi_tich_luy=tiendohoctap.tong_tin_chi_tich_luy,
                diem_trung_binh_tich_luy=tiendohoctap.diem_trung_binh_tich_luy,
                xu_ly_hoc_tap=tiendohoctap.xu_ly_hoc_tap
            )
            db.add(db_tiendohoctap)
            db.commit()
            db.refresh(db_tiendohoctap)
            return db_tiendohoctap
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lỗi khi tạo tiến độ học tập"
            )

    @staticmethod
    def update_tiendohoctap(db: Session, tiendohoctap_id: int, tiendohoctap: schemas.TienDoHocTapUpdate) -> models.TienDoHocTap:
        db_tiendohoctap = TiendohoctapService.get_tiendohoctap(db, tiendohoctap_id)
        
        tiendohoctap_data = tiendohoctap.dict(exclude_unset=True)
        for key, value in tiendohoctap_data.items():
            setattr(db_tiendohoctap, key, value)
            
        try:
            db.commit()
            db.refresh(db_tiendohoctap)
            return db_tiendohoctap
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lỗi khi cập nhật tiến độ học tập"
            )

    @staticmethod
    def delete_tiendohoctap(db: Session, tiendohoctap_id: int) -> models.TienDoHocTap:
        db_tiendohoctap = TiendohoctapService.get_tiendohoctap(db, tiendohoctap_id)
        db.delete(db_tiendohoctap)
        db.commit()
        return db_tiendohoctap

    @staticmethod
    def get_tiendohoctap_detail(db: Session, tiendohoctap_id: int) -> models.TienDoHocTap:
        tiendohoctap = db.query(models.TienDoHocTap).filter(models.TienDoHocTap.id == tiendohoctap_id).first()
        if tiendohoctap is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tiến độ học tập với ID {tiendohoctap_id} không tồn tại"
            )
        return tiendohoctap