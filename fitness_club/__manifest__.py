{
    'name': 'Fitness Club Management',
    'summary': 'Module for fitness club automation: clients, memberships, trainers, schedules and attendance tracking',
    'author': 'Anna Khoroshylova',
    'category': 'Services',
    'license': 'LGPL-3',
    'version': '19.0.1.3.0',

    'depends': [
        'base',
        'web',
        'contacts',
    ],

    'data': [
        'security/fitness_club_security.xml',
        'security/ir.model.access.csv',

        'data/fitness_club_data.xml',

        'views/fitness_plan_views.xml',
        'views/fitness_trainer_views.xml',
        'views/fitness_member_views.xml',
        'views/fitness_subscription_views.xml',
        'views/fitness_class_views.xml',
        'views/fitness_attendance_views.xml',
        'views/res_partner_views.xml',

        'wizards/mass_renew_subscription_wizard_views.xml',
        'wizards/attendance_report_wizard_views.xml',

        'views/menu_views.xml',
    ],

    'demo': [
        'demo/partner_demo.xml',
        'demo/trainer_demo.xml',
        'demo/member_demo.xml',
        'demo/subscription_demo.xml',
        'demo/class_demo.xml',
        'demo/attendance_demo.xml',
    ],

    'installable': True,
    'application': True,

    'images': [
        'static/description/icon.png',
    ],
}
