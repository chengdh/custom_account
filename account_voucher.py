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

import logging
from openerp import netsvc
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp.tools import float_compare
from openerp.report import report_sxw

_logger = logging.getLogger(__name__)
class account_voucher(osv.osv):
  '''
  继承account.voucher对象,修改state,使其适用于工作流
  '''
  _name = 'account.voucher'
  _description = 'Accounting Voucher'
  _inherit = 'account.voucher'


  def _get_where_args_with_workflow(self,cr,uid):
    '''
    获取当前用户工作流审批相关的where 条件
    '''
    matched_groups = None
    pool = self.pool.get('res.users')
    user = pool.browse(cr,uid,uid)
    groups = user.groups_id
    if not groups: return None 
    #根据group_id获取group名称
    model_data_pool = self.pool.get("ir.model.data")
    #部门经理
    group_dept_manager = model_data_pool.get_object(cr,uid,'base','group_dept_manager')
    #店长
    group_shop_manager = model_data_pool.get_object(cr,uid,'base','group_shop_manager')
    #财务经理
    group_account_manager = model_data_pool.get_object(cr,uid,'base','group_account_manager')
    #副总
    group_general_manager = model_data_pool.get_object(cr,uid,'base','group_vice_general_manager')
    #总经理
    group_ceo = model_data_pool.get_object(cr,uid,'base','group_ceo')

    #找出当前用户属于哪个group
    list_b = [group_dept_manager,group_shop_manager,group_account_manager,group_account_manager,group_general_manager,group_ceo]
    matched_groups = list(set(groups).intersection(set(list_b)))
    if not matched_groups: return None

    if group_ceo in matched_groups:
      state = ["dept_manager_approved","vice_general_manager_approved"]
      signal = "ceo_approve"

    if group_general_manager in matched_groups:
      state = ["shop_manager_approved"]
      signal = "vice_general_manager_approve"

    if group_shop_manager in matched_groups:
      state = ["subed_1"]
      signal = "shop_manager_approve"

    if group_dept_manager in matched_groups:
      state = ["subed_2","subed_3"]
      signal = "dept_manager_approve"

    return {"state" : state,"signal" : signal}

  def _next_workflow_signal(self,cr,uid, ids, field_name, arg, context):
    res = {}
    #获取当前用户能查看的expense的状态
    where_args = self._get_where_args_with_workflow(cr,uid)
    for record in self.browse(cr,uid,ids,context):
      res[record.id] = None
      if record.state in where_args['state']: res[record.id] = where_args['signal']

    return res


  _columns = {
      'state':fields.selection(
        [
          ('draft', 'New'),                                                           #草稿
          ('cancel', 'canceled'),                                                   #已驳回
          ('subed_1', 'subflow 1'),                                                  #部门经理已审批
          ('subed_2', 'subflow 2'),                                                  #部门经理已审批
          ('subed_3', 'subflow 3'),                                                  #部门经理已审批
          ('shop_manager_approved', 'Shop Manager Approved'),
          ('dept_manager_approved', 'Department Manager Approved'),
          ('vice_general_manager_approved', 'Vice Manager Approved'),
          ('ceo_approved', 'CEO Approved'),
          ('proforma','Pro-forma'),     #过账
          ('posted','Posted')
          ], 'Status', readonly=True, size=32, track_visibility='onchange',
        help=' * The \'Draft\' status is used when a user is encoding a new and unconfirmed Voucher. \
            \n* The \'Pro-forma\' when voucher is in Pro-forma status,voucher does not have an voucher number. \
            \n* The \'Posted\' status is used when user create voucher,a voucher number is generated and voucher entries are created in account \
            \n* The \'Cancelled\' status is used when user cancel voucher.'),

      "next_workflow_signal" : fields.function(_next_workflow_signal,string="根据当前用户计算下一个workflow signal"),
      }

  def get_waiting_audit_vouchers(self,cr,uid,domain = None,context=None):
    #FIXME 为简单处理,此处为硬编码 
    #1 根据uid获取用户所属group_id
    #2 根据group_id找出对应的工作流state
    #3 根据state获取vouchers列表,返回客户端
    where_args = self._get_where_args_with_workflow(cr,uid)
    if not where_args : return []

    _logger.debug("[state,signal] = " + repr(where_args));
    ids = self.search(cr,uid,[("state","in",where_args["state"]),("type","=","payment"),("journal_id.type","in",["bank","cash"])],context=context)
    if not ids: return []
    vouchers = self.read(cr,uid,ids,context=context)
    _logger.debug("return vouchers =  " + repr(vouchers));
    return vouchers
