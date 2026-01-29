# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class FaceAttendanceController(http.Controller):
    
    @http.route('/cham_cong/identify_employee', type='json', auth='user', methods=['POST'], csrf=False)
    def identify_employee(self, **kw):
        """
        Identify employee from face image
        """
        try:
            image_data = kw.get('image_data')
            result = request.env['nhan_vien'].identify_from_face(image_data)
            return result
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi: {str(e)}'
            }
    
    @http.route('/cham_cong/clock_in_face', type='json', auth='user', methods=['POST'], csrf=False)
    def clock_in_face(self, **kw):
        """
        Clock in using face recognition
        """
        try:
            employee_id = kw.get('employee_id')
            image_data = kw.get('image_data')
            result = request.env['bang_cham_cong'].clock_in_with_face(employee_id, image_data)
            return result
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi: {str(e)}'
            }
    
    @http.route('/cham_cong/clock_out_face', type='json', auth='user', methods=['POST'], csrf=False)
    def clock_out_face(self, **kw):
        """
        Clock out using face recognition
        """
        try:
            employee_id = kw.get('employee_id')
            image_data = kw.get('image_data')
            result = request.env['bang_cham_cong'].clock_out_with_face(employee_id, image_data)
            return result
        except Exception as e:
            return {
                'success': False,
                'message': f'Lỗi: {str(e)}'
            }
