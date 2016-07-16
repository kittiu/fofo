# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    product_qty = fields.Float(
        string='Quantity',
        digits_compute=dp.get_precision('Product Unit of Measure'),
        required=True,
        states={'confirmed': [('readonly', False)],
                'running': [('readonly', False)]},
        readonly=True,
    )

    @api.multi
    def force_done(self):
        self.state = 'done'
