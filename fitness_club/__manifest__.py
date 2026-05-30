{
    'name': 'Fitness Club Management',
    'summary': 'Module for fitness club automation: clients, memberships, trainers, schedules and attendance tracking',
    'author': 'Anna Khoroshylova',
    'category': 'Services',
    'license': 'LGPL-3',
    'version': '19.0.1.1.0',

    'depends': [
        'base',
        'web',
        'contacts',
    ],

    'data': [
        'security/fitness_club_security.xml',
        'security/ir.model.access.csv',
    ],

    'demo': [
        
    ],

    'installable': True,
    'application': True,

    'images': [

    ],
}
