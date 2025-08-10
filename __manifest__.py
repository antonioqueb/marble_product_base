# -*- coding: utf-8 -*-
{
    'name': 'Marble Product Base Management',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Sistema de gestión de inventario para productos de mármol con seguimiento por pieza única',
    'description': ''', ... ''',
    'author': 'Tu Nombre/Empresa',
    'website': 'https://tuempresa.com',
    'depends': [
        'base',
        'product',
        'stock',
        'purchase',
        'purchase_stock', # Muy importante tener esta dependencia
        'uom',
        'web',
        'mail', 
    ],
    'data': [
        # 1. Seguridad primero
        'security/ir.model.access.csv',
        
        # 2. Datos base
        'data/ir_sequence_data.xml',
        'data/product_uom_data.xml',
        
        # 3. Vistas de tus modelos propios (no heredan de otros módulos de forma compleja)
        'views/packing_list_import_views.xml',
        'views/packing_list_import_wizard_views.xml',
        
        # 4. Vistas que heredan de product (generalmente seguro)
        'views/product_template_views.xml',
        'views/product_product_views.xml',
        
        # 5. Vistas que heredan de purchase y stock (las más problemáticas, van al final)
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_quant_views.xml',

        # 6. Menús al final
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/product_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'marble_product_base/static/src/css/marble_styles.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}