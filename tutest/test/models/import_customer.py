# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime,timedelta
import pytz
import re
import json
import xlsxwriter

group_user_index = 17
min_col_number = 3

class Test_customer(models.TransientModel):
    _name = 'test.customer'
    _inherits = {'ir.attachment': 'attachment_id'}

    def find_brand(self, source_string):

        ls_info = source_string.split("/")
        for ls_in in ls_info:
            brand = ls_in.split(" ")
            for item in brand:
                item = item.strip()
                self.env.cr.execute("""with d as (select name, similarity(name, %s) as likenumber from fleet_vehicle_model_brand)
                     select name, likenumber from d where likenumber >=0.4""", [item])
                r = self.env.cr.fetchone()
                if not r:
                    continue
                brand = r[0]

                model = ls_in.replace(item, '').replace('/', '').replace('-', '').replace(' ', '').strip()

                return brand, model
        return '', ''

    def find_phone(self, source_string):
        if source_string:
            source_string = source_string.replace('.', '')
            source_string = source_string.replace('-', '')
            source_string = source_string.replace(' ', '')
            ls_info = source_string.split("/")
            for item in ls_info:
                phone_number = re.findall(r'((?:\d{9,13}))', item)
                if phone_number:
                    return phone_number[0]
        return False

    def find_name(self, source_string):
        ls_info = source_string.split("/")
        for item in ls_info:
            try:
                str(item)
            except:
                return item
        return False

    def test_customer(self):
        content = self.get_value_from_excel_row()
        content = content[1:]

        workbook = xlsxwriter.Workbook('Expenses01.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.set_column(0, 0, 30)
        worksheet.set_column(1, 1, 15)
        worksheet.set_column(2, 2, 15)
        worksheet.set_column(3, 3, 15)
        worksheet.set_column(4, 4, 15)
        worksheet.set_column(5, 5, 15)
        row = 0

        for excelrow in content:
            cont = excelrow
            customer_info = {'source': cont}
            phone = self.find_phone(cont) or ''
            customer_info['phone'] = phone
            if phone:
                cont = cont.replace(phone, '')
            name = self.find_name(cont) or ''
            name = name.strip()
            customer_info['name'] = name
            lst_remove_license_plates = []
            name = name.replace(' - ', '')
            name = name.replace(' -', '')
            search_license_plates = re.findall('[0-9][0-9][A-Z][0-9]{3,12}', name)
            lst_remove_license_plates.extend(search_license_plates)
            for remove_license_plates in lst_remove_license_plates:
                name = name.replace(remove_license_plates, '')
                name = name.strip()

            if name:
                cont = cont.replace(name, '')
            brand, vehicle_model = self.find_brand(cont)
            customer_info['brand'] = brand
            customer_info['model'] = vehicle_model

            worksheet.write(row, 0, excelrow)
            worksheet.write(row, 1, name)
            worksheet.write(row, 2, phone)
            worksheet.write(row, 3, brand)
            worksheet.write(row, 4, vehicle_model)
            row += 1
        workbook.close()

        res = self.env.ref('test.action_test_customer').read([])[0]
        res['res_id'] = self.id
        return res

    @api.multi
    def get_value_from_excel_row(self):
        list_test = []
        excel_data = self.env['read.excel'].read_file(data=self.datas, sheet="Sheet1", path=False)
        if len(excel_data) < 2:
            raise UserError(_(
                'Error: Format file incorrect, you must import file have at least 2 row!'))

        if len(excel_data[0]) < min_col_number:
            raise UserError(_(
                'Error: Format file incorrect, you must import file have at least {} column!').format(
                min_col_number))
        for i in excel_data:
            license_plate = i[1]
            process_string = i[2].replace(license_plate, '')
            list_test.append(process_string)
        return list_test


# # -*- coding: utf-8 -*-
# from odoo import api, fields, models, SUPERUSER_ID, _
# from odoo.exceptions import ValidationError, UserError
# from datetime import datetime,timedelta
# import pytz
# import re
#
# group_user_index = 17
# min_col_number = 18
#
# class Test_customer(models.TransientModel):
#     _name = 'test.customer'
#     _inherits = {'ir.attachment': 'attachment_id'}
#
#
#
#     #
#     # name = fields.Char()
#     # _import_model_name = 'res.partner'
#     # _import_date_format = '%d-%m-%Y'
#     #
#     # template_file_url = fields.Char(compute='_compute_template_file_url',
#     #                                 default=lambda self:
#     #                                 self.env['ir.config_parameter'].
#     #                                 get_param('web.base.url') +
#     #                                 '/bave_import/static/import_template/'
#     #                                 'import_customer.xlsx')
#
#     # @api.multi
#     # def _compute_template_file_url(self):
#     #     base_url = self.env['ir.config_parameter'].get_param('web.base.url')
#     #     url = base_url + '/bave_import/static/import_template/import_customer.xlsx'
#     #     for ip in self:
#     #         ip.template_file_url = url
#
#     def find_brand(self, source_string):
#         ls_brand = []
#         if source_string:
#             ls_info = source_string.split("/")
#             for ls_in in ls_info:
#                 brand = ls_in.split(" ")
#                 ls_brand.extend(brand)
#         for item in ls_brand:
#             result = self.env['fleet.vehicle.model.brand'].search([('name', 'ilike', item)])
#             if result:
#                 return result[0].name
#         return False
#
#     def find_current(self, source_string):
#         ls_current = []
#         if source_string:
#             ls_info = source_string.split("/")
#             for ls_in in ls_info:
#                 current = ls_in.split(" ")
#                 ls_current.extend(current)
#         for item in ls_current:
#             result = self.env['fleet.vehicle.model'].search([('name', 'ilike', item)])
#             if result:
#                 return result[0].name
#         return False
#
#     def find_phone(self, source_string):
#         ls_phone = []
#         if source_string:
#             source_string = source_string.replace('.', '')
#             source_string = source_string.replace('-', '')
#             source_string = source_string.replace(' ', '')
#             ls_info = source_string.split("/")
#             for item in ls_info:
#                 phone_number = re.findall(r'((?:\d{9,13}))', item)
#                 if phone_number:
#                     return phone_number[0]
#         return False
#
#     def find_name(self, source_string):
#         ls_name = []
#         ls_info = source_string.split('/')
#         # print(ls_info)
#         for item in ls_info:
#             try:
#                 str(item)
#             except:
#                 return item
#         return False
#         # return ls_name
#
#     # def find_license_plate(self, source_string):
#     #     ls_license_plate = []
#     #     if source_string:
#     #         ls_info = source_string.split("/")
#     #         for item in ls_info:
#     #             name = re.findall(r'((?:\d{2}[A-Z][0-9]{3,8}))', item)
#     #             if name:
#     #                 ls_license_plate.append(name)
#     #     return ls_license_plate
#
#     def test_customer(self):
#         ls_false = []
#         content = self.get_value_from_excel_row()
#         content = content[1:]
#         for excelrow in content:
#             cont = excelrow
#             # print(cont)
#             customer_info = {'source': cont}
#             name = self.find_name(cont) or ''
#             customer_info['name'] = name
#             customer_info['name'] = customer_info['name'].replace('-', '')
#             if name:
#                 cont = cont.replace(name, '')
#                 myre = re.compile(ur'[0-9]', re.UNICODE)
#                 myre1 = re.compile(ur'[A-Z][0-9]', re.UNICODE)
#                 # customer_info = customer_info['name'].replace(' ', '')
#                 result = myre1.sub('', customer_info['name'])
#                 result1 = myre.sub('', result)
#                 print(result1)
#             phone = self.find_phone(cont) or ''
#             customer_info['phone'] = phone
#
#         return True
#
#     @api.multi
#     def get_value_from_excel_row(self):
#         list_test = []
#         excel_data = self.env['read.excel'].read_file(data=self.datas, sheet="Sheet1", path=False)
#         if len(excel_data) < 2:
#             raise UserError(_(
#                 'Error: Format file incorrect, you must import file have at least 2 row!'))
#
#         if len(excel_data[0]) < min_col_number:
#             raise UserError(_(
#                 'Error: Format file incorrect, you must import file have at least {} column!').format(
#                 min_col_number))
#         for i in excel_data:
#             list_test.append(i[2])
#         return list_test
#
#
#
#
#     #
#     #     partner_model = self.env['res.partner']
#     #     company_id = self.env.user.company_id.id
#     #     if excel_data:
#     #         catg_data = {}
#     #         atts_create = []
#     #         row_count = 1
#     #         for i in excel_data[1:]:
#     #             row_count += 1
#     #             if not i[1]:
#     #                 raise UserError(_('Customer name can not empty, Row %s - Column B') % row_count)
#     #             if not i[2]:
#     #                 raise UserError(_('Customer code can not empty, Row %s - Column C') % row_count)
#     #             exist_code = partner_model.sudo().search([('code', '=', i[2])])
#     #             if exist_code:
#     #                 raise UserError(_('Customer already exists, Row %s - Column C') % row_count)
#     #             if not i[15]:
#     #                 raise UserError(_('Receivable Account can not empty, Row %s - Column P') % row_count)
#     #
#     #             if not i[16]:
#     #                 raise UserError(_('Payable Account can not empty, Row %s - Column Q') % row_count)
#     #
#     #             x_type_1 = u'Cá nhân'
#     #             x_type_2 = u'Công ty'
#     #
#     #             x_type = ''
#     #             if i[0].encode('utf-8').strip().lower() == x_type_1.encode('utf-8').strip().lower():
#     #                 x_type = 'person'
#     #             elif i[0].encode('utf-8').strip().lower() == x_type_2.encode('utf-8').strip().lower():
#     #                 x_type = 'company'
#     #
#     #             if not x_type:
#     #                 raise UserError(_('Type customer does not exists, Row %s - Column A') % row_count)
#     #
#     #             country_id = self.env['res.country'].search([('name', '=', i[4].encode('utf-8').strip())])
#     #             if i[4] and not country_id:
#     #                 raise UserError(_('Không tìm thấy trường quốc gia, Hàng %s - Cột E') % row_count)
#     #             state_id = self.env['res.country.state'].search([('name', '=', i[5].encode('utf-8').strip())])
#     #             if i[5] and not state_id:
#     #                 raise UserError(_('Không tìm thấy trường thành phố, Hàng %s - Cột F') % row_count)
#     #             district_id = self.env['res.country.district'].search([('name', '=', i[6].encode('utf-8').strip())])
#     #             if i[6] and not district_id:
#     #                 raise UserError(_('Không tìm thấy trường Quận/Huyện, Hàng %s - Cột G') % row_count)
#     #             ward_id = self.env['res.country.ward'].search([('name', '=', i[7].encode('utf-8').strip())])
#     #             if i[7] and not ward_id:
#     #                 raise UserError(_('Không tìm thấy trường Phường xã, Hàng %s - Cột G') % row_count)
#     #
#     #             receivable_id = False
#     #             payable_id = False
#     #
#     #             if type(i[15]) is float:
#     #                 x_receivable_id = self.env['account.account'].with_context(show_parent_account=True).search(
#     #                     [('code', '=', str(i[15]).split('.')[0].encode('utf-8')), ('company_id', '=', company_id)])
#     #                 if not x_receivable_id:
#     #                     raise UserError(_('Receivable Account does not exists! Row %s - Column P') % row_count)
#     #                 else:
#     #                     receivable_id = x_receivable_id.id
#     #
#     #             if type(i[15]) is unicode:
#     #                 x_receivable_id = self.env['account.account'].with_context(show_parent_account=True).search(
#     #                     [('code', '=', i[15].encode('utf-8')), ('company_id', '=', company_id)])
#     #                 if not x_receivable_id:
#     #                     raise UserError(_('Receivable Account does not exists! Row %s - Column P') % row_count)
#     #                 else:
#     #                     receivable_id = x_receivable_id.id
#     #
#     #             if type(i[16]) is float:
#     #                 x_code = str(i[16]).split('.')[0].encode('utf-8')
#     #                 x_payable_id = self.env['account.account'].with_context(show_parent_account=True).search(
#     #                         [('code', '=', x_code), ('company_id', '=', company_id)])
#     #                 if not x_payable_id:
#     #                     raise UserError(_('Payable Account does not exists! Row %s - Column Q') % row_count)
#     #                 else:
#     #                     payable_id = x_payable_id.id
#     #
#     #             if type(i[16]) is unicode:
#     #                 x_payable_id = self.env['account.account'].with_context(show_parent_account=True).search(
#     #                     [('code', '=', i[16].encode('utf-8')), ('company_id', '=', company_id)])
#     #                 if not x_payable_id:
#     #                     raise UserError(_('Payable Account does not exists! Row %s - Column Q') % row_count)
#     #                 else:
#     #                     payable_id = x_payable_id.id
#     #
#     #             group_user = False
#     #             if i[group_user_index]:
#     #                 group_users = self.env['btek.partner.group'].search(
#     #                     ['|',('name', '=', i[group_user_index]),('code', '=', i[group_user_index])])
#     #                 group_user = group_users and group_users[0].id or False
#     #                 if not group_user:
#     #                     raise UserError(_(
#     #                         'Partner group "{}" does not exists! Row {}').format(i[group_user_index], row_count))
#     #
#     #             x_sex_1 = u'Nam'
#     #             x_sex_2 = u'Nữ'
#     #             x_sex_3 = u'Khác'
#     #
#     #             x_sex = ''
#     #             if i[9].encode('utf-8').strip().lower() == x_sex_1.encode('utf-8').strip().lower():
#     #                 x_sex = 'male'
#     #             elif i[9].encode('utf-8').strip().lower() == x_sex_2.encode('utf-8').strip().lower():
#     #                 x_sex = 'female'
#     #             elif i[9].encode('utf-8').strip().lower() == x_sex_3.encode('utf-8').strip().lower():
#     #                 x_sex = 'other'
#     #
#     #             title = self.env['res.partner.title'].search([('name', '=', i[11].encode('utf-8').strip())])
#     #             if i[11] and not title:
#     #                 raise UserError(_('Không tìm thấy trường tiêu đề, Hàng %s - Cột L') % row_count)
#     #
#     #             if type(i[10]) != unicode:
#     #                 raise UserError(_('Định dạng nhập trường ngày không đúng, vui lòng nhập định dạng chuỗi như mẫu, Hàng %s - Cột K') % row_count)
#     #             check_birth = ''
#     #             if i[10]:
#     #                 date_birth = str(datetime.strptime(i[10], '%d/%m/%Y'))
#     #                 check_birth = str(datetime.strptime(date_birth, '%Y-%m-%d 00:00:00'))
#     #
#     #             atts_create.append({
#     #                 'company_type': x_type,
#     #                 'name': i[1],
#     #                 'code': i[2],
#     #                 'vat': i[8],
#     #                 'street': i[3],
#     #                 'district_id': district_id[0].id if district_id else False,
#     #                 'country_id': country_id[0].id if country_id else False,
#     #                 'state_id': state_id[0].id if state_id else False,
#     #                 'ward_id': ward_id[0].id if ward_id else False,
#     #                 'sex': x_sex,
#     #                 'date_of_birth': check_birth,
#     #                 'title': title.id,
#     #                 'comment': i[12],
#     #                 'property_account_receivable_id': receivable_id,
#     #                 'property_account_payable_id': payable_id,
#     #                 'customer': True,
#     #                 'phone': i[13],
#     #                 'email': i[14],
#     #                 'group_user': group_user,
#     #             })
#     #         catg_data['atts_create'] = atts_create
#     #         return catg_data
