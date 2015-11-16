# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (c) 2015 - Present Teckzilla Software Solutions Pvt. Ltd. All Rights Reserved
#    Author: [Teckzilla Software Solutions]  <[sales@teckzilla.net]>
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
#    A copy of the GNU General Public License is available at:
#    <http://www.gnu.org/licenses/gpl.html>.
#
##############################################################################

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


class sale_order(models.Model):
    _inherit = "sale.order"

    def _get_shipping_type(self):
        res = super(sale_order, self)._get_shipping_type()
        res.append(('Fedex','Fedex'))
        return res
    
    def _get_service_type_fedex(self):
        return [
             ('EUROPE_FIRST_INTERNATIONAL_PRIORITY','EUROPE_FIRST_INTERNATIONAL_PRIORITY'),
             ('FEDEX_1_DAY_FREIGHT','FEDEX_1_DAY_FREIGHT'),
             ('FEDEX_2_DAY','FEDEX_2_DAY'),
             ('FEDEX_2_DAY_FREIGHT','FEDEX_2_DAY_FREIGHT'),
             ('FEDEX_3_DAY_FREIGHT','FEDEX_3_DAY_FREIGHT'),
             ('FEDEX_EXPRESS_SAVER','FEDEX_EXPRESS_SAVER'),
             ('STANDARD_OVERNIGHT','STANDARD_OVERNIGHT'),
             ('PRIORITY_OVERNIGHT','PRIORITY_OVERNIGHT'),
             ('FEDEX_GROUND','FEDEX_GROUND'),
        ]
     
    shipping_type = fields.Selection(_get_shipping_type, string='Shipping Type', default='All')    
    service_type_fedex = fields.Selection(_get_service_type_fedex, string='Service Type', size=100)
    packaging_type_fedex = fields.Selection([
            ('FEDEX_BOX','FEDEX BOX'),
            ('FEDEX_PAK','FEDEX PAK'),
            ('FEDEX_TUBE','FEDEX_TUBE'),
            ('FEDEX_GROUND','FEDEX_GROUND'),
            ('YOUR_PACKAGING','YOUR_PACKAGING'),
        ], string='Packaging Type', help="What kind of package this will be shipped in", default='YOUR_PACKAGING')
    package_detail_fedex = fields.Selection([
            ('INDIVIDUAL_PACKAGES','INDIVIDUAL_PACKAGES'),
            ('PACKAGE_GROUPS','PACKAGE_GROUPS'),
            ('PACKAGE_SUMMARY','PACKAGE_SUMMARY'),
        ],'Package Detail', default = 'INDIVIDUAL_PACKAGES')
    payment_type_fedex = fields.Selection([
            ('RECIPIENT','RECIPIENT'),
            ('SENDER','SENDER'),
            ('THIRD_PARTY','THIRD_PARTY'),
        ], string='Payment Type', help="Who pays for the rate_request?", default='SENDER')
    physical_packaging_fedex = fields.Selection([
            ('BAG','BAG'),
            ('BARREL','BARREL'),
            ('BOX','BOX'),
            ('BUCKET','BUCKET'),
            ('BUNDLE','BUNDLE'),
            ('CARTON','CARTON'),
            ('TANK','TANK'),
            ('TUBE','TUBE'),
        ], string='Physical Packaging', default='BOX')
        
sale_order()        