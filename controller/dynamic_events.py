# -*- coding:utf-8 -*-
from odoo import http
from odoo.http import request, route


class EventsSnippet(http.Controller):
    """ its pass the latest for events into snippets js file
     to show the data """

    @http.route('/latest_events', type="json", auth="public", website=True)
    def all_events(self):
        events = request.env['manage.events'].search_read(
            [], ['name', 'event_card', 'coordinator', 'start_date', 'end_date'],
            order='start_date desc', limit=10)
        return events

    @route('/slides/<int:id>', type='http', auth='public', website=True)
    def slides(self, id):
        """ when click events it will redirect in to corresponding events"""
        print("hai")
        event_record = request.env['manage.events'].browse(id)
        return request.render('school_management.each_event_snippet',
                              {'event_record': event_record})
