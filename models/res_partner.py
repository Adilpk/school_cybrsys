# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    """ res.partner model add a new field employee_type """
    _inherit = 'res.partner'

    employee_type = fields.Selection(selection=[('teacher', 'Teacher'),
                                                ('school', 'Student'),
                                                ('office staff',
                                                 'Office Staff')],
                                     string='Employee Type')

    @api.constrains('name', 'email')
    def _check_name_and_email(self):
        """ validate name and email in res_partner model """
        count_name = self.search_count([('name', '=', self.name)])
        count_email = self.search_count([('email', '=', self.email)])
        if (count_email > 1 and count_name > 1 and
                self.email is not False and self.name is not False):
            raise ValidationError(_('The email,name already registered,'
                                  ' please use another email!'))
