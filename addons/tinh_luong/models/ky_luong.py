# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime

class KyLuong(models.Model):
    _name = 'ky_luong'
    _description = 'Kỳ lương'
    _order = 'ngay_bat_dau desc'
    _rec_name = 'ten_ky'

    ten_ky = fields.Char(string="Tên kỳ lương", required=True, help="VD: Tháng 1/2026")
    ngay_bat_dau = fields.Date(string="Từ ngày", required=True)
    ngay_ket_thuc = fields.Date(string="Đến ngày", required=True)
    
    trang_thai = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Đã xác nhận'),
        ('paid', 'Đã thanh toán')
    ], string="Trạng thái", default='draft', required=True)
    
    bang_luong_ids = fields.One2many('bang_luong', 'ky_luong_id', string="Bảng lương")
    so_nhan_vien = fields.Integer(string="Số nhân viên", compute='_compute_so_nhan_vien', store=True)
    tong_luong = fields.Float(string="Tổng lương", compute='_compute_tong_luong', store=True)
    tong_luong_formatted = fields.Char(string="Tổng chi trả", compute='_compute_tong_luong_formatted')
    
    @api.depends('bang_luong_ids')
    def _compute_so_nhan_vien(self):
        for record in self:
            record.so_nhan_vien = len(record.bang_luong_ids)
    
    @api.depends('bang_luong_ids', 'bang_luong_ids.tong_luong')
    def _compute_tong_luong(self):
        for record in self:
            record.tong_luong = sum(record.bang_luong_ids.mapped('tong_luong'))
    
    @api.depends('tong_luong')
    def _compute_tong_luong_formatted(self):
        for record in self:
            if record.tong_luong:
                formatted = "{:,.0f}".format(record.tong_luong).replace(',', '.')
                record.tong_luong_formatted = f"{formatted} VNĐ"
            else:
                record.tong_luong_formatted = "0 VNĐ"
    
    @api.model
    def create(self, vals):
        """Override create to ensure computed fields are triggered"""
        record = super(KyLuong, self).create(vals)
        # Force recompute
        record._compute_so_nhan_vien()
        record._compute_tong_luong()
        return record
    
    def action_tao_bang_luong(self):
        """Tạo bảng lương cho tất cả nhân viên"""
        self.ensure_one()
        
        # Xóa bảng lương cũ nếu có
        self.bang_luong_ids.unlink()
        
        # Lấy tất cả nhân viên
        nhan_viens = self.env['nhan_vien'].search([])
        
        # Tạo bảng lương cho mỗi nhân viên
        for nv in nhan_viens:
            self.env['bang_luong'].create({
                'ky_luong_id': self.id,
                'nhan_vien_id': nv.id,
            })
        
        # Force recompute to update counts and totals immediately
        self._compute_so_nhan_vien()
        self._compute_tong_luong()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': f'Đã tạo bảng lương cho {len(nhan_viens)} nhân viên',
                'type': 'success',
                'sticky': False,
            }
        }
    
    def action_xac_nhan(self):
        """Xác nhận kỳ lương"""
        self.write({'trang_thai': 'confirmed'})
    
    def action_thanh_toan(self):
        """Đánh dấu đã thanh toán"""
        self.write({'trang_thai': 'paid'})
