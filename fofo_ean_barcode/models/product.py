#-*- coding: utf-8 -*-
from openerp.osv import fields, osv

class product_product(osv.osv):
    _inherit = 'product.product'

    def _check_ean_key(self, cr, uid, ids, context=None):
        return True

    _constraints = [(_check_ean_key, 'You provided an invalid "EAN13 Barcode" reference. You may use the "Internal Reference" field instead.', ['ean13'])]
