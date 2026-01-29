-- Script to clean up old face recognition module data
-- Run this in psql to remove custom_hr_face_attendance remnants

BEGIN;

-- Delete all ir.model.data records for the old module
DELETE FROM ir_model_data WHERE module = 'custom_hr_face_attendance';

-- Delete model field selections for old models
DELETE FROM ir_model_fields_selection 
WHERE field_id IN (
    SELECT id FROM ir_model_fields 
    WHERE model IN ('face.cham.cong.wizard', 'face.registration', 'face.registration.wizard')
);

-- Delete model fields for old models  
DELETE FROM ir_model_fields 
WHERE model IN ('face.cham.cong.wizard', 'face.registration', 'face.registration.wizard');

-- Delete model constraints
DELETE FROM ir_model_constraint
WHERE model IN (
    SELECT id FROM ir_model 
    WHERE model IN ('face.cham.cong.wizard', 'face.registration', 'face.registration.wizard')
);

-- Delete model relations
DELETE FROM ir_model_relation
WHERE model IN (
    SELECT id FROM ir_model 
    WHERE model IN ('face.cham.cong.wizard', 'face.registration', 'face.registration.wizard')
);

-- Delete the models themselves
DELETE FROM ir_model 
WHERE model IN ('face.cham.cong.wizard', 'face.registration', 'face.registration.wizard');

-- Delete any views related to old module
DELETE FROM ir_ui_view WHERE id IN (
    SELECT res_id FROM ir_model_data 
    WHERE model = 'ir.ui.view' 
    AND module = 'custom_hr_face_attendance'
);

-- Delete any actions related to old module
DELETE FROM ir_act_window WHERE id IN (
    SELECT res_id FROM ir_model_data 
    WHERE model = 'ir.actions.act_window' 
    AND module = 'custom_hr_face_attendance'
);

-- Delete any menu items related to old module
DELETE FROM ir_ui_menu WHERE id IN (
    SELECT res_id FROM ir_model_data 
    WHERE model = 'ir.ui.menu' 
    AND module = 'custom_hr_face_attendance'
);

-- Uninstall the module record if it exists
UPDATE ir_module_module 
SET state = 'uninstalled' 
WHERE name = 'custom_hr_face_attendance';

COMMIT;

-- Verify cleanup
SELECT 'Cleanup completed successfully!' as status;
SELECT COUNT(*) as remaining_records 
FROM ir_model_data 
WHERE module = 'custom_hr_face_attendance';
