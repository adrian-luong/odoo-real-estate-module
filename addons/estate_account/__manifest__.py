{
    'name': "Real Estate Account Module",
    'version': '1.0',
    'depends': ['estate', 'account'],
    'author': "Luong Xuan Trung Dung",
    'category': 'Real Estate',
    'license': 'LGPL-3',
    'summary': "Odoo's tutorial since Chapter 13",
    'installable': True,  # Recommended
    'application': True,  # Recommended to show in the main 'Apps' menu

    # data files always loaded at installation
    'data': [
        # To make your module functional and add a menu, you will need:
        # For access rights
        # 'security/ir.model.access.csv',

        # # For views (forms, trees, etc.)
        # 'views/estate_salesman_views.xml',
        # 'views/estate_property_offer_views.xml',
        # 'views/estate_property_type_views.xml',
        # 'views/estate_property_tag_views.xml',

        # 'views/property/estate_property_form_view.xml',
        # 'views/property/estate_property_views.xml',

        # 'views/estate_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        # 'demo/demo_data.xml',
    ],
}