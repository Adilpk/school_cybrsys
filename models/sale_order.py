# -*- coding: utf-8 -*-
from odoo import models, fields


class SalesOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('admitted', 'Admitted')])
