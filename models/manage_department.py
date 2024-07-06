# -*- coding: utf-8 -*-
from odoo import models, fields


class ManageDepartment(models.Model):
    """Department model"""
    _name = 'manage.department'
    _description = 'Department'
    _inherit = 'mail.thread'

    name = fields.Char(required=True,string='Department')
    hod_id = fields.Many2one('res.partner', string='HOD')
    company_id = fields.Many2one('res.company', string='school')
