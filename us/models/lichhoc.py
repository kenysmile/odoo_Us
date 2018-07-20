# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions

class Lichhoc(models.Model):
    _name = 'us.lichhoc'

    khoahoc = fields.Many2many('us.khoahoc', string='Khóa học')
    gio_1 = fields.Many2many(relation='gio1_project_rel', comodel_name='us.thu', column1='gio1', column2='gio2', string="09:00:00-12:00:00")
    gio_2 = fields.Many2many(relation='gio2_project_rel', comodel_name='us.thu', column1='gio1', column2='gio2', string='14:00:00-16:30:00')
    gio_3 = fields.Many2many(relation='gio3_project_rel', comodel_name='us.thu', column1='gio1', column2='gio2', string="19:00:00-21:00:00")
