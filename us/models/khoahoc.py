# -*- coding: utf-8 -*-

from odoo import fields, models

class Khoahoc(models.Model):
    _name = 'us.khoahoc'

    name = fields.Char(string='Tên khóa học')
    malop = fields.Char(string='Mã lớp')
    ngaykhaigiang = fields.Date(string='Ngày khai giảng')
    ngayketthuc = fields.Date(string='Ngày kết thúc')
    sohvdk = fields.Integer(string='Số học viên đăng ký')
    sohvdihoc = fields.Integer(string='Số học viên đi học')
    tinhtrang = fields.Char('Tình trạng')