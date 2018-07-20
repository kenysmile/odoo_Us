# -*- coding: utf-8 -*-

from odoo import fields, models

class Nhanvien(models.Model):
    _inherit = 'hr.employee'

    mondkdayhoc = fields.Many2many('product.category', string='Môn đăng ký dạy học')