# -*- coding: utf-8 -*-
from odoo import fields, models
import json
import io

from odoo.exceptions import ValidationError
from odoo.fields import Date
from odoo.tools import date_utils
from odoo.tools.misc import xlsxwriter


class ClubWizard(models.TransientModel):
    """ create a transient model for club form wizard"""
    _name = 'club.wizard'
    _description = 'Club wizard'

    club_id = fields.Many2one('manage.clubs', string='Club')
    student_id = fields.Many2one('student.manage', string='Student')

    def button_print(self):
        """ fetch the club, student data from the wizard"""
        today = Date.today()
        data = {
            'club_id': self.club_id.name,
            'student_id': self.student_id.first_name,
            'today': today
        }
        return self.env.ref(
            'school_management.action_report_manage_club').report_action(
            self, data=data)

    def print_xlsx(self):
        """ fetch the wizard data and pass into action_manage.js """
        data = {
            'club_id': self.club_id.name,
            'student_id': self.student_id.first_name,
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'club.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'club Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """ filter the values to print into xlsx"""
        query = """select cl.name,st.first_name,cl.established_date,
                cl.description from manage_clubs as cl inner join 
                manage_clubs_student_manage_rel as mc on cl.id = 
                mc.manage_clubs_id
                inner join student_manage as st on st.id = mc.student_manage_id 
                where 0=0"""
        club = data['club_id']
        student = data['student_id']
        if data['club_id']:
            query = query + f" and cl.name = '{club}'"
        if data['student_id']:
            query = query + f" and st.first_name = '{student}'"
        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()
        if result:

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            sheet = workbook.add_worksheet()
            cell_format = workbook.add_format(
                {'font_size': '12px', 'align': 'center'})
            head = workbook.add_format(
                {'align': 'center', 'bold': True, 'font_size': '20px'})
            txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
            sheet.merge_range('A1:D2', 'Club Report', head)
            sheet.write('E1', self.env.company.name, txt)
            sheet.write('E2', self.env.company.email, txt)
            sheet.set_column(0, 11, 18)
            if data['club_id']:
                sheet.write('A3', 'Club:', cell_format)
                sheet.write('B3', data['club_id'], txt)
            if data['student_id']:
                sheet.write('A4', 'Student:', cell_format)
                sheet.write('B4', student, txt)
            print(data)
            sheet.write('D3', 'Today:', cell_format)
            sheet.write('E3', str(Date.today()), txt)

        else:
            raise ValidationError("Data not Found")
        for i, res in enumerate(result, start=8):
            sheet.write('A6', 'SI.No', cell_format)
            sheet.write(f'A{i}', i - 7, txt)
            sheet.write('B6', 'Description', cell_format)
            sheet.write(f'B{i}', res['description'], txt)
            sheet.write('C6', 'Established Date', cell_format)
            sheet.write(f'C{i}', str(res['established_date']), txt)
            count = 0
            if not data['club_id']:
                count += 1
                sheet.write('D6', 'Club Name', cell_format)
                sheet.write(f'D{i}', str(res['name']), txt)
            if not data['student_id']:
                if count > 0:
                    sheet.write('E6', 'Name', cell_format)
                    sheet.write(f'E{i}', res['first_name'], txt)
                else:
                    sheet.write('D6', 'Name', cell_format)
                    sheet.write(f'D{i}', res['first_name'], txt)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
