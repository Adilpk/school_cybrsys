# -*- coding: utf-8 -*-
from odoo import api, fields, models
import json
import io

from odoo.exceptions import ValidationError
from odoo.fields import Date
from odoo.tools import date_utils
from odoo.tools.misc import xlsxwriter


class StudentWizard(models.TransientModel):
    """ create transient model for filter student details"""
    _name = 'student.wizard'
    _description = ' Student Wizard'

    class_id = fields.Many2one('manage.class', string='Class')
    department_id = fields.Many2one('manage.department',
                                    string='Department')
    all_class_ids = fields.Many2many('manage.class',
                                     string='Classes',
                                     compute='_compute_class_ids')

    @api.depends('department_id')
    def _compute_class_ids(self):
        """" compute the department field for choose corresponding club"""
        for rec in self:
            print(rec)
            if rec.department_id:
                rec.all_class_ids = self.env['manage.class'].search(
                    [('department_id', '=', rec.department_id.id)])

            else:
                rec.all_class_ids = self.env['manage.class'].search([])

    def button_print(self):
        """ fetch the club, student data from the wizard"""
        today = Date.today()
        data = {
            'class_id': self.class_id.name,
            'department_id': self.department_id.name,
            'today': today
        }
        return self.env.ref(
            'school_management.action_report_manage_student').report_action(
            self, data=data)

    def print_xlsx(self):
        """ fetch the data from wizard to filter the data of xlsx"""
        data = {
            'class_id': self.class_id.name,
            'department_id': self.department_id.name
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'student.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'student Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """ fetch the data from database using query"""
        query = """select st.first_name,st.email,st.phone,cl.name as class,
                dt.name as department from student_manage as st inner join 
                manage_class as cl on st.class_id = cl.id inner join 
                manage_department
                as dt on st.department_id = dt.id where 0 = 0"""
        class_name = data['class_id']
        department = data['department_id']
        if data['class_id']:
            query = query + f" and cl.name = '{class_name}'"
        if data['department_id']:
            query = query + f" and dt.name = '{department}'"
        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()
        if result:

            print(result)
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            sheet = workbook.add_worksheet()
            cell_format = workbook.add_format(
                {'font_size': '12px', 'align': 'center'})
            head = workbook.add_format(
                {'align': 'center', 'bold': True, 'font_size': '20px'})
            txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
            sheet.merge_range('A1:E2', 'Student Report', head)
            sheet.write('F1', self.env.company.name, txt)
            sheet.write('F2', self.env.company.email, txt)
            sheet.set_column(0, 11, 18)
            if data['class_id']:
                sheet.write('A3', 'Class:', cell_format)
                sheet.write('B3', data['class_id'], txt)
            if data['department_id']:
                sheet.write('A4', 'Department:', cell_format)
                sheet.write('B4',data['department_id'], txt)
            sheet.write('E3', 'Today:', cell_format)
            sheet.write('F3', str(Date.today()), txt)
        else:
            raise ValidationError("Data not Found")
        for i, res in enumerate(result, start=8):
            sheet.write('A6', 'SI.No', cell_format)
            sheet.write(f'A{i}', i - 7, txt)
            sheet.write('B6', 'Student', cell_format)
            sheet.write(f'B{i}', res['first_name'], txt)
            sheet.write('C6', 'Email', cell_format)
            sheet.write(f'C{i}', str(res['email']), txt)
            sheet.write('D6', 'Phone', cell_format)
            sheet.write(f'D{i}', res['phone'], txt)
            count = 0
            if not data['class_id']:
                count += 1
                sheet.write('E6', 'Class', cell_format)
                sheet.write(f'E{i}', res['class'], txt)
            if not data['department_id']:
                if count > 0:
                    sheet.write('F6', 'Department', cell_format)
                    sheet.write(f'F{i}', res['department'], txt)
                else:
                    sheet.write('E6', 'Dept', cell_format)
                    sheet.write(f'E{i}', res['department'], txt)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()




