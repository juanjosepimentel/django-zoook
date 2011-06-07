# -*- encoding: utf-8 -*-
############################################################################################
#
#    Zoook e-sale for OpenERP, Open Source Management Solution	
#    Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################################

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required

from settings import *
from tools.conn import conn_webservice
from tools.zoook import checkPartnerID, checkFullName, connOOOP, paginationOOOP

"""Orders. All Orders Partner Available"""
@login_required
def orders(request):
    partner_id = checkPartnerID(request)
    full_name = checkFullName(request)
    conn = connOOOP()
    
    values = {}
    total = len(conn.SaleOrder.filter(partner_id=partner_id))
    offset, page_previous, page_next = paginationOOOP(request, total, PAGINATOR_ORDER_TOTAL)

    values = conn.SaleOrder.filter(partner_id=partner_id,offset=offset,limit=PAGINATOR_ORDER_TOTAL,order='id')

    title = _('All Orders')
    metadescription = _('List all orders of %s') % full_name

    return render_to_response("sale/orders.html", {'title':title, 'metadescription':metadescription, 'values':values, 'page_previous':page_previous, 'page_next':page_next}, context_instance=RequestContext(request))

"""Order. Order Detail Partner"""
@login_required
def order(request, order):
    partner_id = checkPartnerID(request)
    full_name = checkFullName(request)
    conn = connOOOP()

    values = conn.SaleOrder.filter(partner_id=partner_id, name=order)
    if len(values) == 0:
        error = _('Not allow view this section or not found. Use navigation menu.')
        return render_to_response("user/error.html", locals(), context_instance=RequestContext(request))

    value = values[0]
    title = _('Order %s') % (value.name)
    metadescription = _('Details order %s') % (value.name)

    return render_to_response("sale/order.html", {'title': title, 'metadescription': metadescription, 'value': value}, context_instance=RequestContext(request))

"""Payment. Payment Order"""
@login_required
def payment(request, order):
    partner_id = checkPartnerID(request)
    full_name = checkFullName(request)
    conn = connOOOP()

    values = conn.SaleOrder.filter(partner_id=partner_id, name=order)
    if len(values) == 0:
        error = _('Not allow view this section or not found. Use navigation menu.')
        return render_to_response("user/error.html", locals(), context_instance=RequestContext(request))

    value = values[0]

    if value.state != 'draft':
        error = _('Your order is running. Contact with us')
        return render_to_response("user/error.html", locals(), context_instance=RequestContext(request))

    payments = conn.PaymentType.filter(esale_payment=True, esale_module__ne='')
    
    title = _('Payment Order %s') % (value.name)
    metadescription = _('Payment order %s') % (value.name)

    return render_to_response("sale/payment.html", {'title': title, 'metadescription': metadescription, 'value': value, 'payments': payments}, context_instance=RequestContext(request))