# -*- coding: utf-8 -*-
from odoo import models, fields


class ManageSubject(models.Model):
    """ subject model"""
    _name = 'manage.subject'
    _description = 'it contain subjects and departments'
    _inherit = 'mail.thread'

    name = fields.Char(required=True, string='Subject')
    department_id = fields.Many2one('manage.department',
                                    string='Department')
