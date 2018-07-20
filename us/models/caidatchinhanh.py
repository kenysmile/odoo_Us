# -*- coding: utf-8 -*-

from odoo import fields, models

class Caidatchinhanh(models.Model):
    _name = 'us.caidatchinhanh'

    name = fields.Char('Chi nhánh')
    diadiem = fields.Many2one('res.company', string='Địa điểm')