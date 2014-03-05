# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from lxml import etree

from openerp import netsvc
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp.tools import float_compare
from openerp.report import report_sxw

class account_voucher(osv.osv):
    '''
    继承account.voucher对象,修改state,使其适用于工作流
    '''
    _name = 'account.voucher'
    _description = 'Accounting Voucher'
    _inherit = 'account.voucher'
    _columns = {
        'state':fields.selection(
            [('draft','Draft'),
             ('cancel','Cancelled'),
             ('approved_1','approved_1'),   #财务经理
             ('approved_2','approved_2'),   #店长
             ('approved_3','approved_3'),   #营运副总
             ('approved_4','approved_4'),   #总经理
             ('proforma','Pro-forma'), #过账

             ('posted','Posted')
            ], 'Status', readonly=True, size=32, track_visibility='onchange',
            help=' * The \'Draft\' status is used when a user is encoding a new and unconfirmed Voucher. \
                        \n* The \'Pro-forma\' when voucher is in Pro-forma status,voucher does not have an voucher number. \
                        \n* The \'Posted\' status is used when user create voucher,a voucher number is generated and voucher entries are created in account \
                        \n* The \'Cancelled\' status is used when user cancel voucher.'),
    }
