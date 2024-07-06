# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.exceptions import ValidationError


class LeaveReport(models.AbstractModel):
    """ create abstract model of Leave report"""
    _name = 'report.school_management.report_leave'

    @api.model
    def _get_report_values(self, docids, data):
        """ manipulate the datas and docs and pass to the templates"""
        query = """select l.subject,l.start_date,l.end_date,st.first_name,
                cl.name from manage_leaves as l inner join student_manage as st 
                on st.user_id = l.student_id inner join manage_class as cl on
                cl.id = st.class_id where 0=0 """
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
        if data['filter2'] == 'student':
            query = query + f" and st.first_name = '{data['student']}'"
        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()
        if result:
            return {
                'doc_ids': docids,
                'data': data,
                'result': result,
            }
        else:
            raise ValidationError("Data not Found!!!")
