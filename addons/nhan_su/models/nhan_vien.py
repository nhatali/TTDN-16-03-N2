from odoo import models, fields, api
from odoo.exceptions import ValidationError
import face_recognition
import numpy as np
import base64
import json
import io
from PIL import Image

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_va_ten' 

    ho_va_ten = fields.Char(string="Họ và tên", required=True) 

    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ngay_sinh = fields.Date("Ngày sinh")
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    dia_chi = fields.Char(string="Địa chỉ")
    bao_hiem_xa_hoi = fields.Char(string="Số BHXH")
    luong = fields.Float(string="Mức lương")
    luong_formatted = fields.Char(string="Tiền lương", compute='_compute_luong_formatted')
    
    @api.depends('luong')
    def _compute_luong_formatted(self):
        for record in self:
            if record.luong:
                # Format: 5.000.000 VNĐ (no decimals)
                formatted = "{:,.0f}".format(record.luong).replace(',', '.')
                record.luong_formatted = f"{formatted} VNĐ"
            else:
                record.luong_formatted = "0 VNĐ"

    # Face Recognition Fields
    face_image = fields.Binary(string="Ảnh khuôn mặt", attachment=True)
    face_encoding = fields.Text(string="Mã hóa khuôn mặt", help="128-dimensional face encoding stored as JSON")
    face_registered = fields.Boolean(string="Đã đăng ký khuôn mặt", compute="_compute_face_registered", store=True)

    @api.depends('face_encoding')
    def _compute_face_registered(self):
        for record in self:
            record.face_registered = bool(record.face_encoding)

    phong_ban_id = fields.Many2one('phong_ban', string="Phòng ban")

    chung_chi_ids = fields.One2many(
        'chung_chi',
        'nhan_vien_id',
        string="Danh sách chứng chỉ"
    )

    cham_cong_ids = fields.One2many(
        'cham_cong',
        'nhan_vien_id',
        string="Lịch sử chấm công"
    )

    lich_su_cong_tac_ids = fields.One2many(
        comodel_name='lich_su_cong_tac',
        inverse_name='nhan_vien_id',
        string="Lịch sử công tác"
    )

    # --- Phần thêm mới cho Văn bản đến ---
    van_ban_den_ids = fields.One2many(
        "van_ban_den",
        "nhan_vien_xu_ly_id",
        string="Văn bản phụ trách"
    )

    van_ban_den_count = fields.Integer(
        string="Số lượng văn bản",
        compute="_compute_vb_count"
    )

    @api.depends("van_ban_den_ids")
    def _compute_vb_count(self):
        for rec in self:
            rec.van_ban_den_count = len(rec.van_ban_den_ids)

    def action_open_van_ban_den(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Văn bản đến",
            "res_model": "van_ban_den",
            "view_mode": "tree,form",
            "domain": [("nhan_vien_xu_ly_id", "=", self.id)],
            "context": {'default_nhan_vien_xu_ly_id': self.id}
        }

    def capture_face(self, image_data):
        """
        Capture and encode face from base64 image data
        :param image_data: Base64 encoded image string
        :return: dict with success status and message
        """
        self.ensure_one()
        
        try:
            # Remove data URL prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert PIL image to numpy array
            image_array = np.array(image)
            
            # Detect faces in the image
            face_locations = face_recognition.face_locations(image_array)
            
            if len(face_locations) == 0:
                raise ValidationError("Không phát hiện khuôn mặt nào trong ảnh. Vui lòng thử lại.")
            
            if len(face_locations) > 1:
                raise ValidationError("Phát hiện nhiều hơn một khuôn mặt. Vui lòng chụp ảnh chỉ có một người.")
            
            # Generate face encoding (128-dimensional vector)
            face_encodings = face_recognition.face_encodings(image_array, face_locations)
            
            if len(face_encodings) == 0:
                raise ValidationError("Không thể mã hóa khuôn mặt. Vui lòng thử lại với ảnh rõ hơn.")
            
            # Store the face encoding as JSON
            encoding_list = face_encodings[0].tolist()
            self.write({
                'face_image': image_data,
                'face_encoding': json.dumps(encoding_list)
            })
            
            return {
                'success': True,
                'message': 'Đăng ký khuôn mặt thành công!'
            }
            
        except ValidationError as e:
            return {
                'success': False,
                'message': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi khi xử lý ảnh: {str(e)}'
            }

    def verify_face(self, image_data, tolerance=0.55):
        """
        Verify captured face against stored encoding
        Args:
            image_data: base64 encoded image
            tolerance: lower = stricter (default 0.55 for good balance)
        """
        self.ensure_one()
        
        if not self.face_encoding:
            return {
                'success': False,
                'match': False,
                'message': 'Nhân viên chưa đăng ký khuôn mặt.'
            }
        
        try:
            # Remove data URL prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert PIL image to numpy array
            image_array = np.array(image)
            
            # Detect faces
            face_locations = face_recognition.face_locations(image_array)
            
            if len(face_locations) == 0:
                return {
                    'success': False,
                    'match': False,
                    'message': 'Không phát hiện khuôn mặt nào.'
                }
            
            # Get face encoding
            face_encodings = face_recognition.face_encodings(image_array, face_locations)
            
            if len(face_encodings) == 0:
                return {
                    'success': False,
                    'match': False,
                    'message': 'Không thể mã hóa khuôn mặt.'
                }
            
            # Load stored encoding
            stored_encoding = np.array(json.loads(self.face_encoding))
            
            # Compare faces
            face_distances = face_recognition.face_distance([stored_encoding], face_encodings[0])
            match = face_distances[0] <= tolerance
            
            # Calculate confidence (distance: 0 = perfect match, 1 = no match)
            # Convert to percentage: 0 distance = 100% confidence
            distance = face_distances[0]
            is_match = match
            confidence = max(0, min(100, (1 - distance) * 100))
            
            return {
                'success': is_match,
                'match': is_match,
                'distance': float(distance),
                'confidence': round(confidence, 1),  # One decimal place
                'message': 'Nhận diện thành công!' if is_match else 'Khuôn mặt không khớp.'
            }
            
        except Exception as e:
            return {
                'success': False,
                'match': False,
                'message': f'Lỗi khi xác thực: {str(e)}'
            }
    
    @api.model
    def identify_from_face(self, image_data, tolerance=0.6):
        """
        Identify employee from face image by comparing with all registered faces
        Args:
            tolerance: lower = stricter (0.6 for easier recognition)
        """
        import face_recognition
        from PIL import Image
        import io
        import numpy as np
        import base64
        import json
        
        # Convert base64 to image
        image_data = image_data.split(',')[1] if ',' in image_data else image_data
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        image_rgb = np.array(image.convert('RGB'))
        
        # Detect face
        face_locations = face_recognition.face_locations(image_rgb)
        if len(face_locations) == 0:
            return {
                'success': False,
                'message': 'Không phát hiện khuôn mặt nào.'
            }
        
        # Get face encoding
        face_encodings = face_recognition.face_encodings(image_rgb, face_locations)
        if len(face_encodings) == 0:
            return {
                'success': False,
                'message': 'Không thể tạo mã hóa khuôn mặt.'
            }
        
        captured_encoding = face_encodings[0]
        
        # Search all registered employees
        employees = self.search([('face_encoding', '!=', False)])
        
        if not employees:
            return {
                'success': False,
                'message': 'Chưa có nhân viên nào đăng ký khuôn mặt.'
            }
        
        best_match = None
        best_distance = 1.0 # Maximum distance
        
        for employee in employees:
            try:
                stored_encoding = np.array(json.loads(employee.face_encoding))
                distance = face_recognition.face_distance([stored_encoding], captured_encoding)[0]
                
                if distance < best_distance:
                    best_distance = distance
                    best_match = employee
            except:
                continue
        
        if best_match and best_distance <= tolerance:
            confidence = max(0, min(100, (1 - best_distance) * 100))
            return {
                'success': True,
                'employee_id': best_match.id,
                'employee_name': best_match.ho_va_ten,
                'employee_code': best_match.ma_dinh_danh or '',
                'confidence': round(confidence, 1),
                'message': f'Nhận diện: {best_match.ho_va_ten}'
            }
        
        return {
            'success': False,
            'message': 'Không nhận diện được nhân viên. Vui lòng đứng gần camera hơn.'
        }