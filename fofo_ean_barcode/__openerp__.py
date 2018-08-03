# -*- coding: utf-8 -*-
{
    'name': "FOFO EAN Barcode",
    'author': "Ecosoft",
    'website': 'http://www.ecosoft.co.th',
    'category': 'Uncategorized',
    'version': '0.1',
    'description': """
* 1) Search for ean13 barcode
* 2) Sales order quotation > create EAN13 Barcode for add product
* 3) Check EAN13 barcode
    """,
    'depends': [
        'sale_stock',
    ],
    'data': [
        'views/product_view.xml',
        'views/sale_view.xml',
    ],
}
