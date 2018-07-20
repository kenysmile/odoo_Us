# -*- coding: utf-8 -*-

from odoo import fields, models

class Phonghoc(models.Model):
    _name = 'us.phonghoc'

    name = fields.Char('Tên phòng học')
    diadiem = fields.Many2one('res.company', string='Địa điểm')
    chinhanh = fields.Many2one('us.caidatchinhanh', string='Chi nhánh')
    succhua = fields.Integer(string='Sức chứa')
    chitietlichhoc = fields.Many2many('us.lichhoc', string='Chi tiết lịch học')