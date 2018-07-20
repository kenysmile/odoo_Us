# -*- coding: utf-8 -*-

from odoo import fields, models

class Loaikhoahoc(models.Model):
    _inherit = 'product.category'

    dsgiaovien = fields.Many2many('hr.employee', string='Danh sách giáo viên')