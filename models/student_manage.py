# -*- coding: utf-8 -*-
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StudentManage(models.Model):
    """ school model"""
    _name = 'student.manage'
    _description = 'student'
    _inherit = 'mail.thread'
    _rec_name = 'first_name'
    _sql_constraints = [('aadhar_number_uniq', 'unique(aadhar_number)',
                         'This aadhar Number is assigned to a previous'
                         ' spot. Please choose another one.!'),
                        ('aadhar_number_length',
                         'check (LENGTH(aadhar_number) = 12)',
                         'Aadhar number should be 12 digit'),
                        ('phone_length',
                         'check (LENGTH(phone) = 10)',
                         'Phone number should be 10 digit')
                        ]

    register_number = fields.Char(string='Register Number', copy=False,
                                  readonly=True)
    admission_number = fields.Char(string='Admission number',
                                   copy=False, readonly=True)
    first_name = fields.Char(required=True, help="school first name")
    last_name = fields.Char(help="school last name")
    father = fields.Char()
    mother = fields.Char()
    communication_as_same = fields.Boolean(default=False, string='Same As')
    communication_address = fields.Text()
    permanent_address = fields.Text()
    email = fields.Char(required=True)
    phone = fields.Char(required=True)
    date_of_birth = fields.Date(string='Date of Birth', required=True)
    age = fields.Char(string='Age', compute='_compute_age',store=True)
    gender = fields.Selection([('Male', 'Male'), ('Female', 'Female')])
    registration_date = fields.Date(default=fields.Date.today())
    photo = fields.Image()
    department_id = fields.Many2one('manage.department',
                                    string='Department')
    class_id = fields.Many2one('manage.class',
                               string='Class')
    file = fields.Binary(string='TC', help='Upload pdf file')
    filename = fields.Char()
    aadhar_number = fields.Char(required=True, copy=False)
    club_ids = fields.One2many('manage.clubs', string='Club Name',
                               inverse_name='student_id')
    company_id = fields.Many2many('res.company', string='Schools',
                                  default=lambda self: self.env.user.company_id)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('registration', 'Registration'),
    ], string='Status', required=True,  copy=False,
        tracking=True, default='draft')
    paper_ids = fields.One2many('manage.paper',
                                'new_id', string='Papers')
    user_id = fields.Integer(string='user')

    @api.model
    def create(self, vals):
        """ Generate Admission numbers"""
        vals['admission_number'] = (self.env['ir.sequence'].next_by_code('my_sequence_code'))
        return super(StudentManage, self).create(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        """ Calculate the school age from the Date of Birth"""
        for record in self:
            if record.date_of_birth:
                d1 = datetime.strptime(str(record.date_of_birth), '%Y-%m-%d').date()
                d2 = date.today()
                age = relativedelta(d2, d1).years
                if age < 5:
                    raise ValidationError("choose correct DOB")
                else:
                    record.age = age

    def button_change_stage(self):
        """ Change the state into registration when click the register button"""
        self.write({'state': 'registration'})
        self.register_number = self.env['ir.sequence'].next_by_code(
            'register_sequence_code')
        last_user_id = self.env['res.users'].search([],order='id desc',limit=1)
        self.user_id = last_user_id

    # @api.constrains('file', 'filename')
    # def get_data(self):
    #     if not self.filename.endswith('.pdf'):
    #         raise ValidationError('your error message')
    #     else:
    #         pass
