# -*- coding: utf-8 -*-
from odoo import models, fields


class ManageAcademicYear(models.Model):
    """its manage the academic years of school"""
    _name = 'manage.academic.year'
    _description = 'it contain academic year'
    _inherit = 'mail.thread'
    _rec_name = 'year'

    year = fields.Char(required=True, string='Academic Year')
