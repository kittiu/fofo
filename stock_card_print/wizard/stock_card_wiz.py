# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-Today Ecosoft Co., Ltd. (http://ecosoft.co.th).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time
from openerp import models, fields, api


class StockCardPrint(models.TransientModel):
    _name = 'stock.card.print'

    start_date = fields.Date(
        string="Start Date",
        default=lambda *a: time.strftime('%Y-01-01'),
        required=True,
    )
    end_date = fields.Date(
        string="End Date",
        default=lambda *a: time.strftime('%Y-%m-%d'),
        required=True,
    )
    product_ids = fields.Many2many(
        'product.product',
        'product_rel_product',
        'product_id',
        'rel_product_id',
        string="Products"
    )
    location_id = fields.Many2one(
        'stock.location',
        string='Warehouse Location',
        required=True,
    )

    @api.multi
    def print_stock_card_report(self):
        data = self.read()[0]
        if not data.get('product_ids', []):
            product_ids = self.env['product.product'].search([]).ids
            data['product_ids'] = product_ids
        return self.env['report'].get_action(self,
            'stock_card_print.stock_card_report_id', data=data)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
