{
    'name': 'Fitness Club Management',
    'summary': 'Module for fitness club automation: clients, memberships, trainers, schedules and attendance tracking',
    'author': 'Anna Khoroshylova',
    'category': 'Services',
    'license': 'LGPL-3',
    'version': '19.0.1.2.0',

    'depends': [
        'base',
        'web',
        'contacts',
    ],

    'data': [
        'security/fitness_club_security.xml',
        'security/ir.model.access.csv',

        'views/fitness_plan_views.xml',
        'views/fitness_trainer_views.xml',
        'views/fitness_member_views.xml',
        'views/fitness_subscription_views.xml',
        'views/fitness_class_views.xml',
        'views/fitness_attendance_views.xml',
        'views/res_partner_views.xml',

        'views/menu_views.xml',
    ],

    'demo': [
        
    ],

    'installable': True,
    'application': True,

    'images': [
        'static/description/icon.png',
    ],
}
