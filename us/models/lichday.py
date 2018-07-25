# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
from datetime import datetime

class Lichday(models.Model):
    _name = 'us.lichday'

    phonghoc = fields.Many2one('us.phonghoc', string='Phòng học')
    appointment_time = fields.Datetime('Appointment time')
    khoahoc = fields.Many2one('us.khoahoc', string='Khóa học')
    tinhtrang = fields.Char('Tình trạng')
    diadiem = fields.Char('Địa điểm')

    @api.onchange('phonghoc')
    def _tinhtrang(self):
        if self.phonghoc:
            self.diadiem = self.phonghoc.diadiem.name
            now = str(datetime.now())
            time_now = now.split('.')[0]
            if time_now > self.appointment_time:
                self.tinhtrang = 'Đã diễn ra'
            else:
                self.tinhtrang = 'Chưa diễn ra'



