# -*- coding: utf-8 -*-
from odoo import fields, models
import json
import io

from odoo.exceptions import ValidationError
from odoo.fields import Date
from odoo.tools import date_utils
from odoo.tools.misc import xlsxwriter


class ExamWizard(models.TransientModel):
    """ exam wizard"""
    _name = 'exam.wizard'
    _description = 'Exam Wizard'

    student_id = fields.Many2one('student.manage', string='Student')
    class_id = fields.Many2one('manage.class', string='Class')
    exam_id = fields.Many2one('manage.exam', string='Exam')

    def button_print(self):
        """ pass the values to print into templates"""
        today = Date.today()
        data = {
            'student_id': self.student_id.first_name,
            'class_id': self.class_id.name,
            'exam_id': self.exam_id.exam,
            'today': today
        }
        print(data)
        return self.env.ref(
            'school_management.action_report_manage_exam').report_action(
            self, data=data)

    def print_xlsx(self):

        data = {
            'student_id': self.student_id.first_name,
            'class_id': self.class_id.name,
            'exam_id': self.exam_id.exam,
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'exam.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Exam Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        query = """select ex.exam,sb.name as subject,pp.pass_mark,pp.max_mark,
                        st.first_name,cl.name as class_name from manage_exam as
                        ex inner join manage_paper as pp on ex.id =  pp.exam_id
                        inner join manage_subject as sb on sb.id = pp.subject_id
                        inner join student_manage as st on st.id = pp.new_id
                        inner join manage_class as cl on cl.id = ex.class_id
                         where 0 = 0"""
        student = data['student_id']
        class_name = data['class_id']
        exam = data['exam_id']
        if data['student_id']:
            query = query + f" and st.first_name = '{student}'"
        if data['class_id']:
            query = query + f" and cl.name = '{class_name}'"
        if data['exam_id']:
            query = query + f" and ex.exam = '{exam}'"
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
            sheet.merge_range('A1:F2', 'Exam Report', head)
            sheet.write('G1', self.env.company.name, txt)
            sheet.write('G2', self.env.company.email, txt)
            sheet.set_column(0, 11, 18)
            if data['student_id']:
                sheet.write('A3', 'Student:', cell_format)
                sheet.write('B3', data['student_id'], txt)
            if data['class_id']:
                sheet.write('A4', 'Class:', cell_format)
                sheet.write('B4', data['class_id'], txt)
            if data['exam_id']:
                sheet.write('A5', 'Exam:', cell_format)
                sheet.write('B5', data['exam_id'], txt)
            sheet.write('F3', 'Today:', cell_format)
            sheet.write('G3', str(Date.today()), txt)
        else:
            raise ValidationError("No Data Found")
        for i, res in enumerate(result, start=9):
            sheet.write('A7', 'SI.No', cell_format)
            sheet.write(f'A{i}', i - 8, txt)
            sheet.write('B7', 'Subject', cell_format)
            sheet.write(f'B{i}', res['subject'], txt)
            sheet.write('C7', 'Pass Mark', cell_format)
            sheet.write(f'C{i}', res['pass_mark'], txt)
            sheet.write('D7', 'Maximum Mark', cell_format)
            sheet.write(f'D{i}', res['max_mark'], txt)
            count = 0
            if not data['student_id']:
                sheet.write('E7', 'Student', cell_format)
                sheet.write(f'E{i}', res['first_name'], txt)
                count += 1
            if not data['class_id']:
                if count == 1:
                    print("2,1")
                    sheet.write('F7', 'Class', cell_format)
                    sheet.write(f'F{i}', res['class_name'], txt)
                    count += 1
                elif count == 0:
                    print("2,2")
                    sheet.write('E7', 'Class', cell_format)
                    sheet.write(f'E{i}', res['class_name'], txt)
                    count += 1
            if not data['exam_id']:
                if count == 2:
                    print("3,1")
                    sheet.write('G7', 'Exam', cell_format)
                    sheet.write(f'G{i}', res['exam'], txt)
                if count == 1:
                    sheet.write('F7', 'Exam', cell_format)
                    sheet.write(f'F{i}', res['exam'], txt)
                elif count == 0:
                    sheet.write('D7', 'Exam', cell_format)
                    sheet.write(f'D{i}', res['exam'], txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
