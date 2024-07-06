# -*- coding : utf-8 -*-
from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo.fields import Date
from odoo.tools import json, date_utils
import io
from odoo.tools.misc import xlsxwriter


class LeaveWizard(models.TransientModel):
    """ create a wizard for make a leave report"""
    _name = 'leave.wizard'
    _description = 'leave wizard'

    filter1 = fields.Selection([('month', 'Month'), ('week', 'Week'),
                                ('day', 'Day'), ('custom', 'Custom')],
                               string='Duration')
    filter2 = fields.Selection([('class', 'Class'),
                                ('student', 'Student')], string='Class/Student')
    start_date = fields.Date(string='Date From')
    end_date = fields.Date(string='Date To')
    class_id = fields.Many2one('manage.class', string='Class')
    student_id = fields.Many2one('student.manage', string='Student')

    def button_print(self):
        """ pass the wizard data into corresponding abstract model"""
        today = Date.today()
        print(today)
        data = {
            'filter1': self.filter1,
            'filter2': self.filter2,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'class': self.class_id.name,
            'student': self.student_id.first_name,
            'today': today
        }
        docids = self.env['manage.leaves'].search([]).ids
        print(docids)
        return self.env.ref(
            'school_management.action_report_manage_leave').report_action(
            docids=docids, data=data)

    def print_xlsx(self):
        """ fetch the wizard data for xlsx report"""
        company = self.env.company
        data = {
            'filter1': self.filter1,
            'filter2': self.filter2,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'class': self.class_id.name,
            'student': self.student_id.first_name,
            'company': company
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'leave.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'leaves Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """ fetch data using query  and pass"""
        query = """select l.subject,l.start_date,l.end_date,st.first_name,
                        cl.name from manage_leaves as l inner join
                        student_manage as st on st.user_id = l.student_id inner
                        join manage_class as cl on cl.id = st.class_id 
                        where 0=0 """
        if data['filter1'] == 'month':
            query = query + (f"and l.start_date BETWEEN date_trunc('month',"
                             f" CURRENT_DATE) and (date_trunc('month',"
                             f" CURRENT_DATE) + interval '1 month - 1 second')")
            print(query)
        if data['filter1'] == 'day':
            query = query + f" and l.start_date = current_date"
            print(query)
        if data['filter1'] == 'week':
            query = query + (f"and l.start_date BETWEEN date_trunc('week',"
                             f" CURRENT_DATE) and (date_trunc('week',"
                             f" CURRENT_DATE) + interval '1 week - 1 second')")
            print(query)
        if data['start_date']:
            start_date = data['start_date']
            query = query + f" and l.start_date >= '{start_date}'"
            print(query)
        if data['end_date']:
            end_date = data['end_date']
            query = query + f" and l.start_date <= '{end_date}'"
            print(query)
        if data['filter2'] == 'class':
            query = query + f" and cl.name = '{data['class']}'"
            print(query)
        if data['filter2'] == 'student':
            query = query + f" and st.first_name = '{data['student']}'"
            print(query)
        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()
        if result:

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            sheet = workbook.add_worksheet()
            cell_format = workbook.add_format(
                {'font_size': '12px','bold': True, 'align': 'center'})
            head = workbook.add_format(
                {'align': 'center', 'bold': True, 'font_size': '20px'})
            txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
            sheet.merge_range('A1:D2', 'Leave Report', head)
            sheet.write('E1', self.env.company.name, txt)
            sheet.write('E2', self.env.company.email, txt)
            sheet.set_column(0, 11, 18)
            if data['filter1']:
                sheet.write('A3', 'Duration:', cell_format)
                sheet.write('B3', data['filter1'], txt)
            if data['filter2'] == 'class':
                sheet.write('A4', 'Class:', cell_format)
                sheet.write('B4', data['class'], txt)
            if data['filter2'] == 'student':
                sheet.write('A5', 'Student:', cell_format)
                sheet.write('B5', data['student'], txt)
            sheet.write('D3', 'Today:', cell_format)
            sheet.write('E3', str(Date.today()), txt)
        else:
            raise ValidationError("Data not Found")

        for i, res in enumerate(result, start=8):
            sheet.write('A6','SI.No', cell_format)
            sheet.write(f'A{i}',i-7, txt)
            sheet.write('B6', 'Subject', cell_format)
            sheet.write(f'B{i}', res['subject'], txt)
            sheet.write('C6', 'Start Date', cell_format)
            sheet.write(f'C{i}', str(res['start_date']), txt)
            sheet.write('D6', 'End Date', cell_format)
            sheet.write(f'D{i}', str(res['end_date']), txt)

            if not data['student']:
                sheet.write('E6', 'Name', cell_format)
                sheet.write(f'E{i}', res['first_name'], txt)
            if not data['class']:
                sheet.write('E6', 'Class', cell_format)
                sheet.write(f'E{i}', res['name'], txt)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
