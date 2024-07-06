# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.exceptions import ValidationError


class StudentReport(models.AbstractModel):
    """ create abstract model of student information"""
    _name = 'report.school_management.report_student'

    @api.model
    def _get_report_values(self, docids, data):
        """manipulate the students information"""
        query = """select st.first_name,st.email,st.phone,cl.name as class,
        dt.name as department from student_manage as st inner join 
        manage_class as cl on st.class_id = cl.id inner join manage_department
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
            return {
                'doc_ids': docids,
                'data': data,
                'result': result
            }
        else:
            raise ValidationError("Data not Found!!!")
