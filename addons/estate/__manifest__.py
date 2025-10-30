{
    'name': "Real Estate Advertisement Module",
    'version': '1.0',
    'depends': ['base'],
    'author': "Luong Xuan Trung Dung",
    'category': 'Real Estate',
    'license': 'LGPL-3',
    'summary': "Odoo's tutorial since Chapter 1",

    # data files always loaded at installation
    'data': [
        # To make your module functional and add a menu, you will need:
        # For access rights
        'security/ir.model.access.csv',

        # For views (forms, trees, etc.)
        'views/res_users_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',

        'views/estate_dashboard.xml',
        'views/estate_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        # 'demo/demo_data.xml',
    ],
    # 'assets': {
    #     'web.assets_frontend': [
    #         ('include', 'web._assets_helpers'),
    #         ('include', 'web._assets_bootstrap'),
    #         ('include', 'web._assets_core'),
    #         'estate/static/src/**/*',
    #     ],
    # },
}