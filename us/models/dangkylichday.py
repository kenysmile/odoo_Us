# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions

class Dangkylichday(models.Model):
    _name = 'us.dangkylichday'

    name = fields.Many2one('res.users', string='Tên')
    dangkytungay = fields.Date(string='Đăng ký từ ngày')
    denngay = fields.Date(string='Đến ngày')
    diadiem = fields.Many2one('res.company', string='Địa điểm')
    dangky = fields.Selection([('1', 'Fulltime ngày trong tuần'), ('2', 'Fulltime buổi tối và cuối tuần'), ('3', 'Parttime')], 'Đăng ký')
    khung_gio_1 = fields.Many2many(relation='khung_gio_1_project_rel', comodel_name='us.thu', column1='khunggio1', column2='khunggio2', string="08:00:00-12:00:00")
    khung_gio_2 = fields.Many2many(relation='khung_gio_2_project_rel', comodel_name='us.thu', column1='khunggio1', column2='khunggio2', string="13:00:00-17:00:00")
    khung_gio_3 = fields.Many2many(relation='khung_gio_3_project_rel', comodel_name='us.thu', column1='khunggio1', column2='khunggio2', string="17:00:00-21:00:00")

    @api.onchange('dangky')
    def _change_dang_ky(self):
        if self.dangky == '1':
            self.khung_gio_1 = self.env['us.thu'].browse([1, 2, 3, 4, 5])
            self.khung_gio_2 = self.env['us.thu'].browse([1, 2, 3, 4, 5])
        if self.dangky == '2':
            self.khung_gio_1 = self.env['us.thu'].browse([6, 7])
            self.khung_gio_2 = self.env['us.thu'].browse([1, 2, 3, 4, 5, 6, 7])
            self.khung_gio_3 = self.env['us.thu'].browse([1, 2, 3, 4, 5, 6, 7])
        if self.dangky == '3':
            self.khung_gio_1 = self.env['us.thu'].browse([])
            self.khung_gio_2 = self.env['us.thu'].browse([])
            self.khung_gio_3 = self.env['us.thu'].browse([])


    @api.model
    def create(self, vals):
        if vals['khung_gio_1'] == [] and vals['khung_gio_2'] == [] and vals['khung_gio_3'] == []:
            raise exceptions.ValidationError("Bạn phải chọn ít nhất 1 giá trị")
        return super(Dangkylichday, self).create(vals)

    @api.multi
    def write(self, vals):
        record = super(Dangkylichday, self).write(vals)
        if vals.get('dangky') == '1':
            self.khung_gio_1 = self.env['us.thu'].browse([1, 2, 3, 4, 5])
            self.khung_gio_2 = self.env['us.thu'].browse([1, 2, 3, 4, 5])
        if self.dangky == '2':
            self.khung_gio_1 = self.env['us.thu'].browse([6, 7])
            self.khung_gio_2 = self.env['us.thu'].browse([1, 2, 3, 4, 5, 6, 7])
            self.khung_gio_3 = self.env['us.thu'].browse([1, 2, 3, 4, 5, 6, 7])
        if self.dangky == '3':
            super(Dangkylichday, self).write(vals)
            if len(self.khung_gio_1) + len(self.khung_gio_2) + len(self.khung_gio_3) == 0:
                raise exceptions.ValidationError("Bạn phải chọn ít nhất 1 giá trị")
        return record
