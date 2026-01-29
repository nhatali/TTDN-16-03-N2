from odoo import models, fields, api


class LichSuCongTac(models.Model):
    _name = 'lich_su_cong_tac'
    _description = 'Lịch sử công tác'
    _order = 'tu_ngay desc, id desc'
    _rec_name = 'name'

    name = fields.Char(string="Tên", compute='_compute_name', store=True)

    nhan_vien_id = fields.Many2one(
        comodel_name='nhan_vien',
        string="Nhân viên",
        required=True,
        ondelete='cascade',
        index=True
    )

    cong_ty = fields.Char(string="Công ty / Đơn vị", required=True)
    chuc_danh = fields.Char(string="Chức danh")
    tu_ngay = fields.Date(string="Từ ngày", required=True)
    den_ngay = fields.Date(string="Đến ngày")
    ly_do_nghi = fields.Char(string="Lý do nghỉ")
    ghi_chu = fields.Text(string="Ghi chú")

    @api.depends('nhan_vien_id', 'cong_ty', 'chuc_danh')
    def _compute_name(self):
        for rec in self:
            if rec.nhan_vien_id and rec.cong_ty:
                if rec.chuc_danh:
                    rec.name = f"{rec.nhan_vien_id.ho_va_ten} - {rec.cong_ty} ({rec.chuc_danh})"
                else:
                    rec.name = f"{rec.nhan_vien_id.ho_va_ten} - {rec.cong_ty}"
            else:
                rec.name = "Lịch sử công tác mới"
