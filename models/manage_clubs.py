# -*- coding: utf-8 -*-
from odoo import models, fields


class ManageClubs(models.Model):
    """Club model"""
    _name = 'manage.clubs'
    _description = 'club'
    _inherit = 'mail.thread'

    name = fields.Char(string='Club', required=True)
    established_date = fields.Date(string='Established')
    description = fields.Text(string='Description')
    student_id = fields.Many2many('student.manage',
                                  string='school Name', ondelete='cascade')

    event_count = fields.Integer(compute='_compute_event_counts')

    def action_events(self):
        """Smart button show the event tree view"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'manage.events',
            'domain': [('club_id', '=', self.ids)],
            'context': "{'create': False}"
        }

    def _compute_event_counts(self):
        """calculate club counts"""
        self.event_count = self.env['manage.events'].search_count(
            [('club_id', '=', self.name)])
