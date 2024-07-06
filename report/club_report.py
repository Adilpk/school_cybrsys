# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.exceptions import ValidationError


class ClubReport(models.AbstractModel):
    """ create abstract model of Leave report"""
    _name = 'report.school_management.report_clubs'

    @api.model
    def _get_report_values(self, docids, data):
        """ manipulate the data and docs and pass to the templates"""
        query = """select cl.name,st.first_name,cl.established_date,
        cl.description from manage_clubs as cl inner join 
        manage_clubs_student_manage_rel as mc on cl.id = mc.manage_clubs_id
        inner join student_manage as st on st.id = mc.student_manage_id 
        where 0=0"""
        club = data['club_id']
        student = data['student_id']
        if data['club_id']:
            query = query + f" and cl.name = '{club}'"
        if data['student_id']:
            query = query + f" and st.first_name = '{student}'"
        print(query)
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
