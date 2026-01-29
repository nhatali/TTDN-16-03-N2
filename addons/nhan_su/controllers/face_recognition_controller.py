# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
import base64
import logging

_logger = logging.getLogger(__name__)


class FaceRecognitionController(http.Controller):
    
    @http.route('/nhan_su/validate_face', type='json', auth='user', methods=['POST'], csrf=False)
    def validate_face(self, **kw):
        """
        Validate face image and return encoding (for new employees)
        """
        try:
            import face_recognition
            from PIL import Image
            import io
            import numpy as np
            
            image_data = kw.get('image_data')
            if not image_data:
                return {'success': False, 'message': 'Không có dữ liệu ảnh.'}
            
            # Convert base64 to image
            image_data = image_data.split(',')[1] if ',' in image_data else image_data
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Resize for faster processing
            max_size = (640, 480)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            image_rgb = np.asarray(image.convert('RGB'))  # asarray faster
            
            # Detect faces with HOG (2-3x faster than CNN)
            face_locations = face_recognition.face_locations(image_rgb, model='hog')
            
            if len(face_locations) == 0:
                return {
                    'success': False,
                    'message': 'Không phát hiện khuôn mặt nào. Vui lòng đảm bảo khuôn mặt của bạn rõ ràng và nhìn thẳng vào camera.'
                }
            
            if len(face_locations) > 1:
                return {
                    'success': False,
                    'message': 'Phát hiện nhiều hơn một khuôn mặt. Vui lòng đảm bảo chỉ có một người trong khung hình.'
                }
            
            # Generate face encoding
            face_encodings = face_recognition.face_encodings(image_rgb, face_locations)
            if len(face_encodings) == 0:
                return {
                    'success': False,
                    'message': 'Không thể tạo mã hóa khuôn mặt. Vui lòng thử lại với ảnh rõ hơn.'
                }
            
            encoding_list = face_encodings[0].tolist()
            encoding_json = json.dumps(encoding_list)
            
            return {
                'success': True,
                'encoding': encoding_json,
                'message': 'Khuôn mặt hợp lệ!'
            }
            
        except Exception as e:
            _logger.error(f'Face validation error: {str(e)}', exc_info=True)
            return {
                'success': False,
                'message': f'Lỗi: {str(e)}'
            }
    
    @http.route('/nhan_su/capture_face', type='json', auth='user', methods=['POST'], csrf=False)
    def capture_face(self, **kw):
        """
        Capture and save employee face encoding
        """
        try:
            employee_id = kw.get('employee_id')
            image_data = kw.get('image_data')
            
            employee = request.env['nhan_vien'].browse(int(employee_id))
            if not employee.exists():
                return {
                    'success': False,
                    'message': 'Nhân viên không tồn tại.'
                }
            
            result = employee.capture_face(image_data)
            return result
            
        except Exception as e:
            _logger.error(f'Face capture error: {str(e)}', exc_info=True)
            return {
                'success': False,
                'message': f'Lỗi: {str(e)}'
            }
    
    @http.route('/nhan_su/verify_face', type='json', auth='user', methods=['POST'], csrf=False)
    def verify_face(self, **kw):
        """
        Verify face against stored encoding
        """
        try:
            employee_id = kw.get('employee_id')
            image_data = kw.get('image_data')
            
            employee = request.env['nhan_vien'].browse(int(employee_id))
            if not employee.exists():
                return {
                    'success': False,
                    'message': 'Nhân viên không tồn tại.'
                }
            
            result = employee.verify_face(image_data)
            return result
            
        except Exception as e:
            _logger.error(f'Face verification error: {str(e)}', exc_info=True)
            return {
                'success': False,
                'message': f'Lỗi: {str(e)}'
            }
    
    @http.route('/nhan_su/identify_face', type='json', auth='user', methods=['POST'], csrf=False)
    def identify_face(self, **kw):
        """
        Identify employee from face image
        """
        try:
            image_data = kw.get('image_data')
            result = request.env['nhan_vien'].identify_from_face(image_data)
            return result
            
        except Exception as e:
            _logger.error(f'Face identification error: {str(e)}', exc_info=True)
            return {
                'success': False,
                'message': f'Lỗi: {str(e)}'
            }
