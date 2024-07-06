# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.exceptions import ValidationError


class EventsReport(models.AbstractModel):
    """ create abstract model for events report"""
    _name = 'report.school_management.report_events'

    @api.model
    def _get_report_values(self, docids, data):
        """ it will get the values of data and doc_ids into this function"""
        query = """select e.name as event,cl.name as club,e.coordinator,
                e.start_date,e.end_date from manage_events as e inner join 
                manage_clubs as cl on cl.id = e.club_id where 0 = 0"""
        print(query)
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
        if result:
            return {
                'doc_ids': docids,
                'data': data,
                'result': result
            }
        else:
            raise ValidationError("Data not Found!!!")
