# -*- coding: utf-8 -*-
from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'

    present = fields.Boolean(string='Present', default=True)
