{
    'name': "Customer",
    'description': """Managing mobile""",
    'summary': """ """,
    'author': "Hieu",
    'version': '0.1',
    
    'depends': ['base'],
    
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/customer.xml',
        'views/product.xml',
        'views/orders.xml',
        'views/detail_orders.xml',

    ],
    
    'installable': True,
    'application': False,
    'auto_install': False,
}