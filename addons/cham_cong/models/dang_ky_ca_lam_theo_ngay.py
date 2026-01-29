from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DangKyCaLamTheoNgay(models.Model):
    _name = 'dang_ky_ca_lam_theo_ngay'
    _description = "Đăng ký ca làm theo ngày"
    _rec_name = 'ma_dot_ngay'

    _order = 'dot_dang_ky_id desc, ngay_lam asc'

    ma_dot_ngay = fields.Char("Mã đợt ngày", required=True)
    dot_dang_ky_id = fields.Many2one('dot_dang_ky', string="Đợt đăng ký", required=True)
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    ngay_lam = fields.Date(string="Ngày làm", required=True)
    ca_lam = fields.Selection([
        ("", ""),
        ("Sáng", "Sáng"),
        ("Chiều", "Chiều"),
        ("Cả ngày", "Cả Ngày"),
    ], string="Ca làm", default="")
    tang_ca = fields.Boolean(string="Tăng ca", default=False, help="Đánh dấu nếu nhân viên đăng ký tăng ca")
    gio_ca = fields.Char(string="Giờ ca", compute='_compute_gio_ca', store=False)
    
    @api.depends('ca_lam')
    def _compute_gio_ca(self):
        shift_times = {
            'Sáng': '7:30 - 11:30',
            'Chiều': '13:30 - 17:30',
            'Cả ngày': '7:30 - 17:30',
        }
        for record in self:
            record.gio_ca = shift_times.get(record.ca_lam, '')

    @api.constrains('ngay_lam', 'dot_dang_ky_id')
    def _check_ngay_lam(self):
        for record in self:
            if record.ngay_lam and record.dot_dang_ky_id:
                if record.ngay_lam < record.dot_dang_ky_id.ngay_bat_dau or record.ngay_lam > record.dot_dang_ky_id.ngay_ket_thuc:
                    raise ValidationError(f'Ngày làm phải nằm trong khoảng thời gian của đợt đăng ký (từ {record.dot_dang_ky_id.ngay_bat_dau} đến {record.dot_dang_ky_id.ngay_ket_thuc})')

    @api.constrains('nhan_vien_id', 'dot_dang_ky_id')
    def _check_nhan_vien_in_dot_dang_ky(self):
        for record in self:
            if record.nhan_vien_id not in record.dot_dang_ky_id.nhan_vien_ids:
                raise ValidationError(f'Nhân viên {record.nhan_vien_id.ho_va_ten} không thuộc đợt đăng ký này!')
