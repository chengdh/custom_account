# -*- coding: utf-8 -*-

{
    'name': 'custom account',
    'version': '0.1',
    'category': 'Accounting & Finance',
    'description': """custome account_voucher module""",
    'author': 'chengdh (cheng.donghui@gmail.com)',
    'website': '',
    'license': 'AGPL-3',
    'depends': ['account_voucher'],
    'data': [
      'security/ir_rules.xml',
      "account_voucher_view.xml",
      "account_voucher_workflow.xml",
      "custom_account_data.xml",
      "report.xml",
      ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'web':True,
    'css': [],
    'js': [],
    'xml': [],

}

