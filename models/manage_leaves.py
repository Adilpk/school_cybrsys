# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api
from datetime import datetime


class ManageLeaves(models.Model):
    """ Leave model"""
    _name = 'manage.leaves'
    _description = 'manage leaves'
    _rec_name = 'student_id'
    _inherit = 'mail.thread'

    student_id = fields.Many2one('res.users', string='Name',
                                 default=lambda self: self.env.user)
    subject = fields.Char()
    start_date = fields.Date(string='Date From')
    end_date = fields.Date(string='Date To')
    total_date = fields.Integer('Number of Days',
                                compute='_compute_total_date', store=True)
    leave_type = fields.Boolean(default=False, string='Half Day')
    reason = fields.Text(string='Reason')

    def action_attendance_calculation(self):
        """ check the school is absent or not """
        print('hello')
        current_date = datetime.today().date()
        for rec in self.env['res.users'].search([]):
            rec.present = True

        for rec in self.env['manage.leaves'].search([]):
            print(rec, 'record leave')
            if rec.start_date <= current_date <= rec.end_date:
                student_name = rec.student_id
                print('school absent',
                      self.env['res.users'].browse(student_name.id).name)
                self.env['res.users'].browse(student_name.id).present = False

    @api.onchange('start_date', 'end_date')
    def _compute_total_date(self):
        """Calculate total number of leaves from the start date and end date."""
        for record in self:
            if record.start_date and record.end_date:
                total_days = 0
                current_date = record.start_date
                while current_date < record.end_date:
                    if current_date.weekday() < 5:
                        total_days = total_days + 1
                    current_date = current_date + timedelta(days=1)
                record.total_date = total_days
            else:
                record.total_date = 0
