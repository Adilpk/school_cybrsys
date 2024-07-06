# -*- coding: utf-8 -*-
from odoo import fields, models
import json
import io

from odoo.exceptions import ValidationError
from odoo.fields import Date
from odoo.tools import date_utils
from odoo.tools.misc import xlsxwriter


class EventWizard(models.TransientModel):
    """ create a wizard for filter events details"""
    _name = 'event.wizard'
    _description = 'Event Wizard'

    filter1 = fields.Selection([('month', 'Month'), ('week', 'Week'),
                                ('day', 'Day'), ('custom', 'Custom')],
                               string='Duration',
                               default='month')
    club_id = fields.Many2one('manage.clubs', string='Club')
    start_date = fields.Date(string='Date From')
    end_date = fields.Date(string='Date To')

    def button_print(self):
        """ fetch the data from wizard to print pdf data"""
        today = Date.today()
        data = {
            'filter1': self.filter1,
            'club_id': self.club_id.name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'today': today
        }

        return self.env.ref(
            'school_management.action_report_manage_events').report_action(
            self, data=data)

    def print_xlsx(self):
        """ fetch the datas from wiard for xlsx report"""
        data = {
            'filter1': self.filter1,
            'club_id': self.club_id.name,
            'start_date': self.start_date,
            'end_date': self.end_date
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'event.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Event Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """" fetch the data from the database and print the xlsx report"""
        query = """select e.name as event,cl.name as club,e.coordinator,
                        e.start_date,e.end_date from manage_events as e 
                        inner join 
                        manage_clubs as cl on cl.id = e.club_id where 0 = 0"""
        club = data['club_id']
        if data['club_id']:
            query = query + f" and cl.name='{club}'"
            print(query)
        if data['filter1'] == 'month':
            query = query + (f" and e.start_date BETWEEN date_trunc('month',"
                             f" CURRENT_DATE) and (date_trunc('month',"
                             f" CURRENT_DATE) + interval '1 month - 1 second')")
            print(query)
        if data['filter1'] == 'day':
            query = query + f" and e.start_date = current_date"
            print(query)
        if data['filter1'] == 'week':
            query = query + (f" and e.start_date BETWEEN date_trunc('week',"
                             f" CURRENT_DATE) and (date_trunc('week',"
                             f" CURRENT_DATE) + interval '1 week - 1 second')")
            print(query)
        if data['start_date'] and data['end_date']:
            start_date = data['start_date']
            end_date = data['end_date']
            query = (query +
                     f" and e.start_date >= '{start_date}' and e.start_date <="
                     f" '{end_date}'")
        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()
        print(result)
        if result:

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            sheet = workbook.add_worksheet()
            cell_format = workbook.add_format(
                {'font_size': '12px', 'align': 'center'})
            head = workbook.add_format(
                {'align': 'center', 'bold': True, 'font_size': '20px'})
            txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
            sheet.merge_range('A1:E2', 'Event Report', head)
            sheet.write('F1', self.env.company.name, txt)
            sheet.write('F2', self.env.company.email, txt)
            sheet.set_column(0, 11, 18)
            if data['filter1']:
                sheet.write('A3', 'Duration:', cell_format)
                sheet.write('B3', data['filter1'], txt)
            if data['club_id']:
                sheet.write('A4', 'Club:', cell_format)
                sheet.write('B4', data['club_id'], txt)
            sheet.write('E3', 'Today:', cell_format)
            sheet.write('F3', str(Date.today()), txt)
        else:
            raise ValidationError("Data not Found")

        for i, res in enumerate(result, start=8):
            sheet.write('A6', 'SI.No', cell_format)
            sheet.write(f'A{i}', i - 7, txt)
            sheet.write('B6', 'Event', cell_format)
            sheet.write(f'B{i}', res['event'], txt)
            sheet.write('C6', 'Conducted By', cell_format)
            sheet.write(f'C{i}', str(res['coordinator']), txt)
            sheet.write('D6:G6', 'Start Date', cell_format)
            sheet.write(f'D{i}', str(res['start_date']), txt)
            sheet.write('E6', 'Start Date', cell_format)
            sheet.write(f'E{i}', str(res['end_date']), txt)
            if not data['club_id']:
                sheet.write('F6', 'Club', cell_format)
                sheet.write(f'F{i}', res['club'], txt)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

