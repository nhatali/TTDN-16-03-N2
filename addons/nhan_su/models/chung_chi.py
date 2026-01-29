from odoo import models, fields


class ChungChi(models.Model):
    _name = 'chung_chi'
    _description = 'Chứng chỉ'

    name = fields.Char(string="Tên chứng chỉ", required=True)
    ma_chung_chi = fields.Char(string="Mã chứng chỉ")
    ngay_cap = fields.Date(string="Ngày cấp")
    ngay_het_han = fields.Date(string="Ngày hết hạn")
    noi_cap = fields.Char(string="Nơi cấp")
    ghi_chu = fields.Text(string="Ghi chú")

    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string="Nhân viên",
        required=True,
        ondelete='cascade',
        index=True
    )
