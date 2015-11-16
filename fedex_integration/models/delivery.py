# -*- encoding: utf-8 -*-
##############################################################################
#Copyright (c) 2015 - Present Teckzilla Software Solutions Pvt. Ltd. All Rights Reserved
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

class delivery_carrier(models.Model):
    _inherit = "delivery.carrier"
    
    is_fedex = fields.Boolean('Is FedEx', help="If the field is set to True, it will consider it as FedEx service type.")
    
class product_category_shipping(models.Model):
    _inherit = "product.category.shipping"
    
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
        
    service_type_fedex = fields.Selection(_get_service_type_fedex, string='Service Type Fedex') 
    
product_category_shipping()

class product_product_shipping(models.Model):
    _inherit = "product.product.shipping"
    
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
        
    service_type_fedex = fields.Selection(_get_service_type_fedex, string='Service Type Fedex')
        
product_product_shipping()