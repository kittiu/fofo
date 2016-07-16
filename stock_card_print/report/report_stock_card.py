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
import datetime
from openerp import api, fields, models


class ReportStockCardReport(models.AbstractModel):
    _name = 'report.stock_card_print.stock_card_report_id'

    def _get_initial_balance_qty(self, product_id, location_id, start_date):
        self._cr.execute('''
            SELECT
                move.id,
                move.origin as doc_number,
                move.product_uom_qty as quantity,
                0.0 as balance,
                p.name as customer,
                to_char(move.date, 'MM/DD/YYYY') as date,
                move.location_dest_id as location_dest_id
            FROM
                stock_move move
            LEFT JOIN
                res_partner p on (p.id=move.partner_id)
            WHERE
                move.product_id = %s AND
                (move.location_id = %s or location_dest_id=%s) AND
                move.date < %s
            ORDER BY
                move.date asc
        ''', (product_id, location_id, location_id, start_date))
        move_result = self._cr.dictfetchall()

        balance_qty = 0.0
        for res in move_result:
            destionation_address = self.env['stock.location'].\
                browse(res['location_dest_id'])
            if destionation_address.usage == 'customer':
                balance_qty = balance_qty - res['quantity']
                res['quantity'] = -1 * res['quantity']
                res['balance'] = balance_qty
            else:
                balance_qty = balance_qty + res['quantity']
                res['balance'] = balance_qty
        return balance_qty or 0.0

    def _get_product_line(self, data):
        result = {}
        start_date = data['start_date']
        end_date = data['end_date']
        location = self.env['stock.location'].browse(data['location_id'][0])
        products = self.env['product.product'].browse(data['product_ids'])
        for product in products:
            init_balance_qty = self._get_initial_balance_qty(
                                    product.id, location.id, start_date)
            self._cr.execute('''
                SELECT
                    move.id,
                    move.origin as doc_number,
                    move.product_uom_qty as quantity,
                    0.0 as balance,
                    p.name as customer,
                    to_char(move.date, 'MM/DD/YYYY') as date,
                    move.location_dest_id as location_dest_id
                FROM
                    stock_move move
                LEFT JOIN
                    res_partner p on (p.id=move.partner_id)
                WHERE
                    move.product_id = %s AND
                    (move.location_id = %s or location_dest_id=%s) AND
                    move.date >= %s AND
                    move.date <= %s
                ORDER BY
                    move.date asc
            ''', (product.id, location.id, location.id, start_date, end_date))
            move_result = self._cr.dictfetchall()

            balance_qty = init_balance_qty
            for res in move_result:
                destionation_address = self.env['stock.location'].\
                    browse(res['location_dest_id'])
                if destionation_address.usage == 'customer':
                    balance_qty = balance_qty - res['quantity']
                    res['quantity'] = -1 * res['quantity']
                    res['balance'] = balance_qty
                else:
                    balance_qty = balance_qty + res['quantity']
                    res['balance'] = balance_qty
            move_result.insert(0, {'balance': init_balance_qty,
                                   'doc_number': False,
                                   'quantity': False,
                                   'customer': False,
                                   'date': False,
                                   'opening_balance': True})
            move_result.append({'balance': False,
                                'doc_number': False,
                                'quantity': balance_qty,
                                'customer': False,
                                'date': False,
                                'closing_balance': True})
            key = (location, product)
            result[key] = move_result
        return result

    @api.multi
    def render_html(self, data):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d')
        start_date = start_date.strftime('%m/%d/%Y')
        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d')
        end_date = end_date.strftime('%m/%d/%Y')
        lines = self._get_product_line(data)
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs,
            'data': data,
            'get_product_line': lines,
            'start_date': start_date,
            'end_date': end_date
        }
        return self.env['report'].render(
            'stock_card_print.stock_card_report_id',
            values=docargs)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
