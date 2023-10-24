{
    'name': 'Real Estate',
    'summary': """The Real Estate""",
    'author': 'BachTN',
    'version': '0.1',
    'category': 'Uncategorized',
    'depends': [
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/real_estate_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menu_views.xml',
    ],
    # 'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
}