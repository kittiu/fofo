#-*- coding: utf-8 -*-
from openerp import models, fields, api

class sale_order(models.Model):
    _inherit = 'sale.order'

    ean13 = fields.Char('EAN13 Barcode')

    @api.onchange('ean13')
    def _onchange_ean13(self):
        if not self.ean13:
            return {}
        Product = self.env['product.product']
        Line = self.env['sale.order.line']
        product = Product.search([('ean13', '=', self.ean13)])
        for pd in product:
            line = Line.new({'product_id': pd.id})
            self.order_line += line
        self.ean13 = False
