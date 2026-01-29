-- SQL Script to clean up orphaned face attendance data
-- Run this before updating modules

-- Delete orphaned model data
DELETE FROM ir_model WHERE model IN (
    'face.cham.cong.wizard',
    'face.registration',
    'face.registration.wizard',
    'don_vi',
    'chuc_vu',
    'chung_chi_bang_cap',
    'danh_sach_chung_chi_bang_cap'
);

-- Delete orphaned model fields
DELETE FROM ir_model_fields WHERE model IN (
    'face.cham.cong.wizard',
    'face.registration',
    'face.registration.wizard',
    'don_vi',
    'chuc_vu',
    'chung_chi_bang_cap',
    'danh_sach_chung_chi_bang_cap'
);

-- Delete orphaned model data entries
DELETE FROM ir_model_data WHERE model IN (
    'ir.model',
    'ir.model.fields',
    'ir.model.fields.selection',
    'ir.model.access',
    'ir.ui.view'
) AND module IN ('custom_hr_face_attendance', 'face_id');

-- Delete orphaned views
DELETE FROM ir_ui_view WHERE model IN (
    'face.cham.cong.wizard',
    'face.registration',
    'face.registration.wizard'
);

-- Delete orphaned access rules  
DELETE FROM ir_model_access WHERE model_id IN (
    SELECT id FROM ir_model WHERE model IN (
        'face.cham.cong.wizard',
        'face.registration',
        'face.registration.wizard',
        'don_vi',
        'chuc_vu',
        'chung_chi_bang_cap',
        'danh_sach_chung_chi_bang_cap'
    )
);

-- Delete orphaned menu items
DELETE FROM ir_ui_menu WHERE action LIKE '%face%';
