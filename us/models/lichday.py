# -*- coding: utf-8 -*-

from odoo import fields, models

class Lichday(models.Model):
    _inherit = 'calendar.event'

    phonghoc = fields.Many2one('us.phonghoc', string='Phòng học')
