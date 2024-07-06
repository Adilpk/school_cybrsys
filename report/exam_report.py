# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.exceptions import ValidationError


class ExamReport(models.AbstractModel):
    """ create abstract model for exam report"""
    _name = 'report.school_management.report_exam'

    @api.model
    def _get_report_values(self, docids, data):
        """ get the values from the wizard and this method used to get the
        database values from the table passing sql query and pass these values
        into pdf template also check the values from the wizard side """
        query = """select ex.exam,sb.name as subject,pp.pass_mark,pp.max_mark,
                st.first_name,cl.name as class_name from manage_exam as ex
                inner join manage_paper as pp on ex.id =  pp.exam_id inner join
                manage_subject as sb on sb.id = pp.subject_id inner join
                student_manage as st on st.id = pp.new_id inner join
                manage_class as cl on cl.id = ex.class_id where 0 = 0"""
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
        if result:
            return {
                'doc_ids': docids,
                'data': data,
                'result': result
            }
        else:
            raise ValidationError("Data not Found!!!")
