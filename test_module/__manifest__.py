{
    'name': 'Testing',
    'version': '17.0.1.0.0',
    'category': 'Hidden',
    'summary': 'Test concept',
    'description': """
        This is for testing
    """,
    'author': 'Test',
    'depends': ['base'],
    'post_init_hook': 'send_install_notification',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}