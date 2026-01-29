# -*- coding: utf-8 -*-
from odoo import models, fields, api

class BangLuong(models.Model):
    _name = 'bang_luong'
    _description = 'Bảng lương'
    _order = 'ky_luong_id desc, nhan_vien_id'
    _rec_name = 'nhan_vien_id'

    # Relations
    ky_luong_id = fields.Many2one('ky_luong', string="Kỳ lương", required=True, ondelete='cascade')
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    
    # Lương cơ bản
    luong_co_ban = fields.Float(string="Lương cơ bản", related='nhan_vien_id.luong', store=True)
    luong_theo_ngay = fields.Float(string="Lương/ngày", compute='_compute_luong', store=True)
    
    # Dữ liệu chấm công (computed)
    so_ngay_cong = fields.Integer(string="Số ngày công", compute='_compute_cham_cong', store=True, readonly=False)
    so_ngay_nghi = fields.Integer(string="Ngày nghỉ", compute='_compute_cham_cong', store=True, readonly=False)
    tong_phut_di_muon = fields.Float(string="Tổng phút đi muộn", compute='_compute_cham_cong', store=True, readonly=False)
    tong_phut_ve_som = fields.Float(string="Tổng phút về sớm", compute='_compute_cham_cong', store=True, readonly=False)
    so_gio_tang_ca = fields.Float(string="Số giờ tăng ca", compute='_compute_cham_cong', store=True, readonly=False)
    
    # Debug info
    so_ban_ghi_cham_cong = fields.Integer(string="Số record chấm công", compute='_compute_cham_cong', store=True)
    
    # Tính tiền (computed)
    tien_phat_di_muon = fields.Float(string="Phạt đi muộn", compute='_compute_luong', store=True)
    tien_phat_ve_som = fields.Float(string="Phạt về sớm", compute='_compute_luong', store=True)
    tien_tru_nghi = fields.Float(string="Trừ nghỉ", compute='_compute_luong', store=True)
    tien_thuong_tang_ca = fields.Float(string="Thưởng tăng ca", compute='_compute_luong', store=True)
    tong_luong = fields.Float(string="Tổng lương", compute='_compute_luong', store=True)
    
    # Display formatted
    tong_luong_formatted = fields.Char(string="Lương thực nhận", compute='_compute_luong_formatted')
    
    @api.depends('ky_luong_id.ngay_bat_dau', 'ky_luong_id.ngay_ket_thuc', 'nhan_vien_id')
    def _compute_cham_cong(self):
        """Tính toán dữ liệu chấm công từ bang_cham_cong - Optimized"""
        BangChamCong = self.env['bang_cham_cong']
        
        for record in self:
            if not record.ky_luong_id or not record.nhan_vien_id:
                record.so_ngay_cong = 0
                record.so_ngay_nghi = 0
                record.tong_phut_di_muon = 0
                record.tong_phut_ve_som = 0
                record.so_gio_tang_ca = 0
                record.so_ban_ghi_cham_cong = 0
                continue
            
            # Optimized query - single search with all conditions
            domain = [
                ('nhan_vien_id', '=', record.nhan_vien_id.id),
                ('ngay_cham_cong', '>=', record.ky_luong_id.ngay_bat_dau),
                ('ngay_cham_cong', '<=', record.ky_luong_id.ngay_ket_thuc)
            ]
            attendances = BangChamCong.search(domain)
            
            # Số ngày công
            record.so_ngay_cong = len(attendances)
            record.so_ban_ghi_cham_cong = len(attendances)  # Debug
            
            if not attendances:
                record.tong_phut_di_muon = 0
                record.tong_phut_ve_som = 0
                record.so_gio_tang_ca = 0
                record.so_ngay_nghi = 0
                continue
            
            # Aggregate in-memory (faster than multiple ORM calls)
            record.tong_phut_di_muon = sum(att.phut_di_muon for att in attendances)
            record.tong_phut_ve_som = sum(att.phut_ve_som for att in attendances)
            
            # Count overtime efficiently
            so_ngay_tang_ca = sum(1 for att in attendances if att.tang_ca == 'Có')
            record.so_gio_tang_ca = so_ngay_tang_ca * 2  # 2h per OT day
            
            # Tính số ngày nghỉ
            if record.ky_luong_id.ngay_bat_dau and record.ky_luong_id.ngay_ket_thuc:
                total_days = (record.ky_luong_id.ngay_ket_thuc - record.ky_luong_id.ngay_bat_dau).days + 1
                record.so_ngay_nghi = total_days - record.so_ngay_cong
            else:
                record.so_ngay_nghi = 0
    
    @api.depends('luong_co_ban', 'so_ngay_cong', 'tong_phut_di_muon', 'tong_phut_ve_som', 
                 'so_gio_tang_ca', 'so_ngay_nghi')
    def _compute_luong(self):
        """Tính toán lương thực nhận"""
        for record in self:
            # ===== XỬ LÝ NHÂN VIÊN CHƯA LÀM VIỆC =====
            # Nếu nhân viên chưa làm (0 ngày công) thì lương = 0
            if record.so_ngay_cong == 0:
                record.luong_theo_ngay = 0
                record.tien_phat_di_muon = 0
                record.tien_phat_ve_som = 0
                record.tien_tru_nghi = 0
                record.tien_thuong_tang_ca = 0
                record.tong_luong = 0
                continue
            # ===== KẾT THÚC XỬ LÝ =====
            
            # Lương theo ngày (chia cho 26 ngày làm việc/tháng)
            record.luong_theo_ngay = record.luong_co_ban / 26 if record.luong_co_ban else 0
            
            # Phạt đi muộn: 10,000 VNĐ/phút
            record.tien_phat_di_muon = (record.tong_phut_di_muon / 60) * 10000
            
            # Phạt về sớm: 10,000 VNĐ/phút
            record.tien_phat_ve_som = (record.tong_phut_ve_som / 60) * 10000
            
            # Trừ nghỉ không phép
            record.tien_tru_nghi = record.so_ngay_nghi * record.luong_theo_ngay
            
            # Thưởng tăng ca: 100,000 VNĐ/giờ
            record.tien_thuong_tang_ca = record.so_gio_tang_ca * 100000
            
            # Tổng lương = Lương CB + Thưởng - Phạt - Trừ nghỉ
            record.tong_luong = (
                record.luong_co_ban
                + record.tien_thuong_tang_ca
                - record.tien_phat_di_muon
                - record.tien_phat_ve_som
                - record.tien_tru_nghi
            )
    
    @api.depends('tong_luong')
    def _compute_luong_formatted(self):
        """Format lương hiển thị"""
        for record in self:
            if record.tong_luong:
                formatted = "{:,.0f}".format(record.tong_luong).replace(',', '.')
                record.tong_luong_formatted = f"{formatted} VNĐ"
            else:
                record.tong_luong_formatted = "0 VNĐ"
