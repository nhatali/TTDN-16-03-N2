from odoo import models, fields

class VanBanDen(models.Model):
    _name = "van_ban_den"
    _description = "Quản lý văn bản đến"

    name = fields.Char("Số ký hiệu/Tên văn bản", required=True)
    trich_yeu = fields.Text("Trích yếu nội dung")
    
    nhan_vien_xu_ly_id = fields.Many2one(
        "nhan_vien",
        string="Nhân viên xử lý",
        required=True
    )
    nhan_vien_ky_id = fields.Many2one(
        "nhan_vien",
        string="Người ký"
    )