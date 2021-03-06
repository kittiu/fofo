# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Ecosoft Co., Ltd. (http://ecosoft.co.th).
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
{
    'name': 'Run Clean Transaction Data Query',
    'category': 'tools',
    'version': '1.0',
    'author': 'Ecosoft',
    'depends': ['base', 'mail'],
    'website': 'http://www.ecosoft.co.th',
    'description': """ 
This module runs the PSQL query from front end.The Query is configured from Setting/Run Query/Sql Query menu.User can run multiple queries at same time from  Setting/Run Query/Run Sql Query menu.
This module only support Delete, Update, Alter queries.
    """,
    'data': [
            'security/ir.model.access.csv',
            'data/res.data.clean.line.csv',
            'views/clean_data_view.xml'
    ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
