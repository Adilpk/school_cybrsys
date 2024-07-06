# -*- coding: utf-8 -*-
from odoo import models, fields


class ManageClass(models.Model):
    """Mange class model"""
    _name = 'manage.class'
    _description = 'it contain class name and department'
    _inherit = 'mail.thread'

    name = fields.Char(required=True,
                       string='Class')
    department_id = fields.Many2one('manage.department',
                                    string='Department')
    hod_id = fields.Many2one(related='department_id.hod_id', string='HOD')
    school_id = fields.Many2one('res.company',
                                string='Current School')
