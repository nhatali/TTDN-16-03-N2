from odoo import models, fields, api


class ChamCong(models.Model):
    _name = 'cham_cong'
    _description = 'Chấm công'
    _order = 'ngay desc'
    _rec_name = 'name'

    name = fields.Char(string="Tên", compute='_compute_name', store=True)

    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string="Nhân viên",
        required=True,
        ondelete='cascade',
        index=True
    )

    ngay = fields.Date(string="Ngày", required=True)
    gio_vao = fields.Datetime(string="Giờ vào")
    gio_ra = fields.Datetime(string="Giờ ra")

    trang_thai = fields.Selection(
        [
            ('present', 'Có mặt'),
            ('late', 'Đi muộn'),
            ('leave', 'Nghỉ phép'),
            ('absent', 'Vắng'),
        ],
        string="Trạng thái",
        default='present'
    )

    ghi_chu = fields.Text(string="Ghi chú")

    @api.depends('nhan_vien_id', 'ngay')
    def _compute_name(self):
        for rec in self:
            if rec.nhan_vien_id and rec.ngay:
                rec.name = f"{rec.nhan_vien_id.ho_va_ten} - {rec.ngay}"
            else:
                rec.name = "Chấm công mới"

    _sql_constraints = [
        ('unique_nhan_vien_ngay', 'UNIQUE(nhan_vien_id, ngay)', 
         'Nhân viên đã có bản ghi chấm công cho ngày này!')
    ]