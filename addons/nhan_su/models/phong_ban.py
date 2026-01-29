from odoo import models, fields, api


class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa thông tin phòng ban'
    _rec_name = 'ten_phong'

    ma_phong = fields.Char(string="Mã phòng ban", required=True)
    ten_phong = fields.Char(string="Tên phòng ban", required=True)
    mo_ta = fields.Text(string="Mô tả")
    ngay_thanh_lap = fields.Date(string="Ngày thành lập")

    truong_phong_id = fields.Many2one(
        'nhan_vien',
        string="Trưởng phòng"
    )

    nhan_vien_ids = fields.One2many(
    'nhan_vien',
    'phong_ban_id', 
    string="Danh sách nhân viên"
    )
