odoo.define('nhan_su.face_capture', function (require) {
    'use strict';

    var AbstractField = require('web.AbstractField');
    var core = require('web.core');
    var fieldRegistry = require('web.field_registry');
    var rpc = require('web.rpc');

    var _t = core._t;

    var FaceCaptureWidget = AbstractField.extend({
        template: 'FaceCaptureWidget',
        events: {
            'click .o_face_capture_btn': '_onClickCapture',
            'click .o_face_stop_btn': '_onClickStop',
        },

        init: function () {
            this._super.apply(this, arguments);
            this.video = null;
            this.stream = null;
            this.capturing = false;
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.video = self.$('.o_face_video')[0];
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
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'
                }
            })
                .then(function (stream) {
                    self.stream = stream;
                    self.video.srcObject = stream;
                    self.video.play();
                    self.capturing = true;
                    self.$('.o_face_capture_btn').text(_t('Chụp ảnh'));
                    self.$('.o_face_stop_btn').show();
                    self.$('.o_face_status').text(_t('Camera đã sẵn sàng. Hãy chụp ảnh khuôn mặt của bạn.'));
                })
                .catch(function (err) {
                    self.$('.o_face_status').text(_t('Lỗi: Không thể truy cập camera. ') + err.message);
                    console.error('Camera error:', err);
                });
        },

        _stopCamera: function () {
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
            this.$('.o_face_capture_btn').text(_t('Bắt đầu quét khuôn mặt'));
            this.$('.o_face_stop_btn').hide();
        },

        _captureImage: function () {
            var canvas = document.createElement('canvas');
            canvas.width = this.video.videoWidth;
            canvas.height = this.video.videoHeight;
            var ctx = canvas.getContext('2d');
            ctx.drawImage(this.video, 0, 0);
            return canvas.toDataURL('image/jpeg', 0.95);
        },

        _onClickCapture: function (ev) {
            ev.preventDefault();
            ev.stopPropagation();

            var self = this;

            if (!this.capturing) {
                this._startCamera();
                return;
            }

            // Capture image from video
            var imageData = this._captureImage();

            // Get employee ID from record
            var employeeId = this.recordData.id || this.res_id;

            this.$('.o_face_status').text(_t('Đang xử lý nhận diện khuôn mặt...'));
            this.$('.o_face_capture_btn').prop('disabled', true);

            if (employeeId) {
                // Existing employee - save directly to database
                rpc.query({
                    route: '/nhan_su/capture_face',
                    params: {
                        employee_id: employeeId,
                        image_data: imageData
                    }
                }).then(function (result) {
                    self.$('.o_face_capture_btn').prop('disabled', false);

                    if (result.success) {
                        self.$('.o_face_status').text(result.message).css('color', 'green');
                        self._stopCamera();
                        self.trigger_up('reload');
                    } else {
                        self.$('.o_face_status').text(result.message).css('color', 'red');
                    }
                }).guardedCatch(function (error) {
                    self.$('.o_face_capture_btn').prop('disabled', false);
                    var errorMsg = error.data && error.data.message ? error.data.message : error.message;
                    self.$('.o_face_status').text(_t('Lỗi: ') + errorMsg).css('color', 'red');
                });
            } else {
                // New employee - validate and store in form
                rpc.query({
                    route: '/nhan_su/validate_face',
                    params: {
                        image_data: imageData
                    }
                }).then(function (result) {
                    self.$('.o_face_capture_btn').prop('disabled', false);

                    if (result.success) {
                        // Update form fields - strip data URI prefix for binary field
                        var imageBase64 = imageData.split(',')[1] || imageData;

                        self.trigger_up('field_changed', {
                            dataPointID: self.dataPointID,
                            changes: {
                                face_image: imageBase64,
                                face_encoding: result.encoding
                            },
                        });

                        self.$('.o_face_status').text('✓ Khuôn mặt đã được quét! Hãy lưu nhân viên để hoàn tất đăng ký.').css('color', 'green');
                        self._stopCamera();

                        // Enhanced image display - use full data URI
                        setTimeout(function () {
                            var $formView = self.$el.closest('.o_form_view');
                            var $imageField = $formView.find('.o_field_widget[name="face_image"]');

                            if ($imageField.length) {
                                var $img = $imageField.find('img');
                                if ($img.length) {
                                    $img.attr('src', imageData);
                                } else {
                                    $imageField.html('<img src="' + imageData + '" class="img img-responsive" style="max-width: 100%; max-height: 200px;"/>');
                                }
                            }
                        }, 200);
                    } else {
                        self.$('.o_face_status').text(result.message).css('color', 'red');
                    }
                }).guardedCatch(function (error) {
                    self.$('.o_face_capture_btn').prop('disabled', false);
                    var errorMsg = error.data && error.data.message ? error.data.message : error.message;
                    self.$('.o_face_status').text(_t('Lỗi: ') + errorMsg).css('color', 'red');
                });
            }
        },

        _onClickStop: function (ev) {
            ev.preventDefault();
            ev.stopPropagation();
            this._stopCamera();
            this.$('.o_face_status').text(_t('Đã dừng camera.'));
        },
    });

    fieldRegistry.add('face_capture', FaceCaptureWidget);

    return FaceCaptureWidget;
});
