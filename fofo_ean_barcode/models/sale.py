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
            product_line = Line.product_id_change(self.pricelist_id.id, product.id, 1, False, 0, False, product.name_template, self.partner_id.id, False, True, self.date_order, False, self.fiscal_position, False)
            product_line['value'].update({'product_id': pd.id, 'product_uom_qty': 1, 'discount': 0,
                                          'state': 'draft'})
            line = Line.new(product_line['value'])
            self.order_line += line
        self.ean13 = False
