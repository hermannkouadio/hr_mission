# -*- encoding: utf-8 -*-
{
    'name': 'HR Mission',
    'description': """
Use to manage employee mission outside company.
=================================================================================================
""",
    # Your information
    'author': 'Anicet Eric Kouame and Hermann KOUADIO',
    'website': 'https://github.com/hermannkouadio',
    'license': 'AGPL-3',
    'version': '8.0',
    'depends': ['base', 'hr', 'account_accountant', 'report', 'calendar', 'resource'],
    'category': 'Human Resources',
    'description': 'This module manage the most important asset in your company: People Mission.',
    'summary': 'This module will help you to mastering human resources mission outside your company.',
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'views/hr_mission_view.xml',
        'views/mission_type_view.xml',
        'views/expense_view.xml',
        'reports/reports.xml',
    ],
    'images': [
        'images/icon.png'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
