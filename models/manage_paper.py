# -*- coding: utf-8 -*-
from odoo import fields, models


class ManagePaper(models.Model):
    """ Exam peper model"""
    _name = 'manage.paper'
    _description = 'Exam Papers'
    _rec_name = 'subject_id'

    subject_id = fields.Many2one('manage.subject',
                                 string='Subject', required=True)
    pass_mark = fields.Float(string='Pass Mark', required=True)
    max_mark = fields.Float(string='Max Mark', required=True)
    exam_id = fields.Many2one('manage.exam', string='Exam')
    new_id = fields.Many2one('student.manage', string='Student')
