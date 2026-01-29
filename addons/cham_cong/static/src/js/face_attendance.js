odoo.define('cham_cong.face_attendance', function (require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var _t = core._t;

    var FaceAttendanceAction = AbstractAction.extend({
        template: 'FaceAttendanceAction',
        events: {
            'click .o_clock_in_btn': '_onClickClockIn',
            'click .o_clock_out_btn': '_onClickClockOut',
            'click .o_start_camera_btn': '_onClickStartCamera',
            'click .o_stop_camera_btn': '_onClickStopCamera',
        },

        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.video = null;
            this.stream = null;
            this.capturing = false;
            this.identifiedEmployee = null;
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.video = self.$('.o_attendance_video')[0];
                self._startCamera();
            });
        },

        destroy: function () {
            this._stopCamera();
            return this._super.apply(this, arguments);
        },

        _startCamera: function () {
            var self = this;
            if (this.capturing) {
                return;
            }

            navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: 'user'
                }
            })
                .then(function (stream) {
                    self.stream = stream;
                    self.video.srcObject = stream;
                    self.video.play();
                    self.capturing = true;
                    self.$('.o_start_camera_btn').hide();
                    self.$('.o_stop_camera_btn').show();
                    self.$('.o_attendance_status').text(_t('Camera đã sẵn sàng. Đứng trước camera để nhận diện.'));

                    // Start continuous identification
                    self._startIdentification();
                })
                .catch(function (err) {
                    self.$('.o_attendance_status').text(_t('Lỗi: Không thể truy cập camera. ') + err.message);
                    console.error('Camera error:', err);
                });
        },

        _stopCamera: function () {
            if (this.identificationInterval) {
                clearInterval(this.identificationInterval);
                this.identificationInterval = null;
            }

            if (this.stream) {
                this.stream.getTracks().forEach(function (track) {
                    track.stop();
                });
                this.stream = null;
            }
            if (this.video) {
                this.video.srcObject = null;
            }
            this.capturing = false;
            this.$('.o_start_camera_btn').show();
            this.$('.o_stop_camera_btn').hide();
        },

        _captureImage: function () {
            var canvas = document.createElement('canvas');
            canvas.width = this.video.videoWidth;
            canvas.height = this.video.videoHeight;
            var ctx = canvas.getContext('2d');
            ctx.drawImage(this.video, 0, 0);
            return canvas.toDataURL('image/jpeg', 0.70); // Reduced from 0.85 for better performance
        },

        _startIdentification: function () {
            var self = this;
            var locked = false; // Lock to prevent UI flicker
            var lockTimeout = null;

            // Identify every 3 seconds (reduced frequency for stability)
            this.identificationInterval = setInterval(function () {
                if (!self.capturing || locked) {
                    return;
                }

                var imageData = self._captureImage();

                rpc.query({
                    route: '/cham_cong/identify_employee',
                    params: {
                        image_data: imageData
                    }
                }).then(function (result) {
                    if (result.success) {
                        // Lock UI for 5 seconds to prevent flicker
                        locked = true;
                        if (lockTimeout) clearTimeout(lockTimeout);
                        lockTimeout = setTimeout(function () { locked = false; }, 5000);

                        self.identifiedEmployee = {
                            id: result.employee_id,
                            name: result.employee_name,
                            employee_code: result.employee_code || '',
                            confidence: result.confidence
                        };

                        self.$('.o_employee_info').show();
                        self.$('.o_employee_name').text(result.employee_name);
                        self.$('.o_employee_code').text(result.employee_code || 'N/A');
                        self.$('.o_employee_department').text(result.phong_ban || 'Chưa có');
                        self.$('.o_confidence').text(result.confidence.toFixed(1) + '%');

                        self.$('.o_clock_in_btn, .o_clock_out_btn').prop('disabled', false);
                        self.$('.o_attendance_status').text('✓ Đã nhận diện: ' + result.employee_name).css('color', 'green');
                    } else if (!locked) {
                        // Only hide if not locked
                        self.identifiedEmployee = null;
                        self.$('.o_employee_info').hide();
                        self.$('.o_clock_in_btn, .o_clock_out_btn').prop('disabled', true);
                        self.$('.o_attendance_status').text('Đang chờ nhận diện...').css('color', '#666');
                    }
                }).guardedCatch(function (error) {
                    if (!locked) {
                        console.error('Identification error:', error);
                    }
                });
            }, 3000); // 3 seconds interval
        },

        _onClickStartCamera: function (ev) {
            ev.preventDefault();
            this._startCamera();
        },

        _onClickStopCamera: function (ev) {
            ev.preventDefault();
            this._stopCamera();
            this.$('.o_attendance_status').text('Đã dừng camera.');
        },

        _onClickClockIn: function (ev) {
            ev.preventDefault();

            var self = this;

            if (!this.identifiedEmployee) {
                this.$('.o_attendance_status').text('Vui lòng đứng trước camera để nhận diện.').css('color', 'orange');
                return;
            }

            var imageData = this._captureImage();

            this.$('.o_attendance_status').text('Đang xử lý chấm công vào...').css('color', 'blue');
            this.$('.o_clock_in_btn').prop('disabled', true);

            rpc.query({
                route: '/cham_cong/clock_in_face',
                params: {
                    employee_id: this.identifiedEmployee.id,
                    image_data: imageData
                }
            }).then(function (result) {
                self.$('.o_clock_in_btn').prop('disabled', false);

                if (result.success) {
                    self.$('.o_attendance_status').text(result.message).css('color', 'green');
                    self.$('.o_last_action').text('Chấm công vào: ' + result.time);

                    // Show notification
                    self.displayNotification({
                        title: _t('Thành công!'),
                        message: result.message,
                        type: 'success'
                    });
                } else {
                    self.$('.o_attendance_status').text(result.message).css('color', 'red');

                    self.displayNotification({
                        title: _t('Lỗi'),
                        message: result.message,
                        type: 'danger'
                    });
                }
            }).guardedCatch(function (error) {
                self.$('.o_clock_in_btn').prop('disabled', false);
                self.$('.o_attendance_status').text(_t('Lỗi kết nối: ') + error.message).css('color', 'red');
            });
        },

        _onClickClockOut: function (ev) {
            ev.preventDefault();

            var self = this;

            if (!this.identifiedEmployee) {
                this.$('.o_attendance_status').text('Vui lòng đứng trước camera để nhận diện.').css('color', 'orange');
                return;
            }

            var imageData = this._captureImage();

            this.$('.o_attendance_status').text('Đang xử lý chấm công ra...').css('color', 'blue');
            this.$('.o_clock_out_btn').prop('disabled', true);

            rpc.query({
                route: '/cham_cong/clock_out_face',
                params: {
                    employee_id: this.identifiedEmployee.id,
                    image_data: imageData
                }
            }).then(function (result) {
                self.$('.o_clock_out_btn').prop('disabled', false);

                if (result.success) {
                    self.$('.o_attendance_status').text(result.message).css('color', 'green');
                    self.$('.o_last_action').text('Chấm công ra: ' + result.time);

                    // Show notification
                    self.displayNotification({
                        title: _t('Thành công!'),
                        message: result.message,
                        type: 'success'
                    });
                } else {
                    self.$('.o_attendance_status').text(result.message).css('color', 'red');

                    self.displayNotification({
                        title: _t('Lỗi'),
                        message: result.message,
                        type: 'danger'
                    });
                }
            }).guardedCatch(function (error) {
                self.$('.o_clock_out_btn').prop('disabled', false);
                self.$('.o_attendance_status').text(_t('Lỗi kết nối: ') + error.message).css('color', 'red');
            });
        },
    });

    core.action_registry.add('face_attendance_action', FaceAttendanceAction);

    return FaceAttendanceAction;
});
