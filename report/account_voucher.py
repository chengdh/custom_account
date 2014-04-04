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

from openerp.report import report_sxw
from netsvc import Service

def to_big_rmb(money=0,rmb=None):
    '''
    人民币小写转大写
    '''
    big = [u'零', u'壹', u'贰', u'叁', u'肆', u'伍', u'陆', u'柒', u'捌', u'玖']  
    rmb = [u'分', u'角', u'圆', u'拾', u'佰', u'仟', u'万', u'拾', u'佰', u'仟', u'亿', u'拾', u'佰', u'仟', u'万',u'拾', u'佰', u'仟',u'万',u'亿']  
    if rmb:
        rmb = rmb

    #转成字符串
    str_money = str( int(money * 100) )[::-1]
    big_money = ''

    #拼大写金额
    for i in xrange(len(str_money)):
        n = ord(str_money[i]) - ord('0')
        big_money = big[n] + rmb[i] + big_money  

    #去掉零ls
    rule = (u'零仟', u'零',
            u'零佰', u'零',
            u'零拾', u'零',
            u'零亿', u'亿',
            u'零万', u'万',
            u'零元', u'元',
            u'零角', u'零',
            u'零分', u'零',
            u'零零', u'零',
            u'零亿', u'亿',
            u'零零', u'零',
            u'零万', u'万',
            u'零零', u'零',
            u'零圆', u'圆',
            u'亿万', u'亿',
            u'零', u'',
            u'圆$', u'圆整')

    for i in xrange(0,len(rule),2):
        big_money = big_money.replace(rule[i], rule[i+1])  

    return big_money


class voucher(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(voucher, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({'to_big_rmb': to_big_rmb})

#del Service._services['report.voucher_print']
report_sxw.report_sxw('report.voucher.print.new','account.voucher','addons/custom_account/report/account_voucher.mako',parser=voucher)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
