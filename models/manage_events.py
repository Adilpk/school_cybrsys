# -*- coding: utf-8 -*-
from odoo import api, models, fields
from datetime import datetime


class ManageEvents(models.Model):
    """  Events Model"""
    _name = 'manage.events'
    _description = 'events'
    _inherit = 'mail.thread'

    name = fields.Char(string='Event')
    event_card = fields.Image(string='Card', attachment=True)
    club_id = fields.Many2one('manage.clubs', string='Club')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    venue_id = fields.Many2one('res.company', string='Venue',
                               default=lambda self: self.env.user.company_id)
    coordinator = fields.Char(string='coordinator')
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[
        ('new', 'New'),
        ('announced', 'Announced'),
        ('ended', 'ended'),
    ], string='Status', required=True, copy=False,
        tracking=True, default='new')

    @api.constrains('state')
    def get_data(self):
        """ when event state is move to ended state then it will archive"""
        if self.state == 'ended':
            self.write({'active': False})

    def send_partners(self):
        """ send the mail for all employees"""
        employee_to_send = self.env['hr.employee'].search([])
        print(employee_to_send)
        email_list = [rec.work_email for rec in employee_to_send]
        return ",".join(email_list)

    def action_email_employees(self):
        """" send emails into all employees"""
        print(self)
        for rec in self.env['manage.events'].search([]):
            if rec.start_date:
                if (rec.start_date.date() - datetime.today().date()).days == 2:
                    mail_template = self.env.ref(
                        'school_management.email_template_event')
                    mail_template.send_mail(rec.id, force_send=True)
                    print('mailsend')
