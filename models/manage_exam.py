# -*- coding: utf-8 -*-
from odoo import fields, models


class ManageExam(models.Model):
    """ Exam model"""
    _name = 'manage.exam'
    _description = 'Exams'
    _inherit = 'mail.thread'
    _rec_name = 'exam'

    exam = fields.Char(string='Exam', required=True)
    class_id = fields.Many2one('manage.class', string='Class',
                               required=True)
    paper_ids = fields.One2many('manage.paper',
                                'exam_id', string='Papers')

    def button_exam(self):
        """ exam button """
        print(self)
