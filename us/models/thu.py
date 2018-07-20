# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions

class Thu(models.Model):
    _name = 'us.thu'

    name = fields.Char('Thứ')