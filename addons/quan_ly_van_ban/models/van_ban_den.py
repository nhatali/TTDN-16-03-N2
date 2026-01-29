from odoo import models, fields, api
from datetime import date

from odoo.exceptions import ValidationError

class VanBanDen(models.Model):
    _name = 'van_ban_den'
    _description = 'Bảng chứa thông tin văn bản đến'
    _rec_name = 'ten_van_ban'

    so_van_ban_den = fields.Char("Số hiệu văn bản", required=True)
    ten_van_ban = fields.Char("Tên văn bản", required=True)
    so_hieu_van_ban = fields.Char("Số hiệu văn bản", required=True)
    noi_gui_den = fields.Char("Nơi gửi đến")
    
    # Quan hệ với nhân viên (từ module nhan_su)
    nhan_vien_xu_ly_id = fields.Many2one(
        'nhan_vien',
        string="Nhân viên xử lý",
        help="Nhân viên phụ trách xử lý văn bản này"
    )
    nhan_vien_ky_id = fields.Many2one(
        'nhan_vien',
        string="Người ký",
        help="Nhân viên ký văn bản"
    )

