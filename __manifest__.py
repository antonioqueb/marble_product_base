# -*- coding: utf-8 -*-
{
    'name': 'Marble Product Base Management',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Sistema de gestión de inventario para productos de mármol con seguimiento por pieza única',
    'description': '''
        Módulo base para la gestión avanzada de inventario de productos de mármol.
        
        Características principales:
        - Creación automática de productos únicos por placa
        - Importación masiva desde Packing Lists
        - Seguimiento por número de serie único
        - Gestión de lotes personalizados
        - Integración completa con compras y inventario
        - Trazabilidad completa desde proveedor hasta venta
        
        Este módulo permite manejar cada placa de mármol como un producto único
        con sus propias dimensiones, costos y características específicas.
    ''',
    'author': 'Tu Nombre/Empresa',
    'website': 'https://tuempresa.com',
    'depends': [
        'base',
        'product',
        'stock',
        'purchase',
        'purchase_stock',
        'uom',
        'web',
        'mail', 
    ],
    'data': [
        # Seguridad
        'security/ir.model.access.csv',
        
        # Datos base
        'data/ir_sequence_data.xml',
        'data/product_uom_data.xml',
        
        # Vistas - orden corregido
        'views/product_template_views.xml',
        'views/product_product_views.xml',
        'views/packing_list_import_views.xml',
        'views/packing_list_import_wizard_views.xml',
        'views/purchase_order_views.xml',
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
    'external_dependencies': {
        'python': [],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
    'sequence': 10,
    # 'images': ['static/description/icon.png'],
}