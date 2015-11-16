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
from openerp.osv import osv
from openerp.exceptions import UserError
from openerp.addons.base_module_shipping.models.miscellaneous import Address
import cStringIO
from base64 import b64decode
from base64 import b64encode
import Image
import StringIO
import binascii
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfgen import canvas
import base64
import os
from openerp.addons.fedex.services.rate_service import FedexRateServiceRequest
from openerp.addons.fedex.services.ship_service import FedexProcessShipmentRequest
from openerp.addons.fedex.config import FedexConfig
import logging
logger = logging.getLogger(__name__)

class stock_picking(models.Model):
    _inherit = 'stock.picking'
    
    def _get_shipping_type(self):
        res = super(stock_picking, self)._get_shipping_type()
        res.append(('Fedex','Fedex'))
        return res
    
    @api.multi
    def return_fedex_shipping_rate(self, dropoff_type_fedex, service_type_fedex, packaging_type_fedex, package_detail_fedex, payment_type_fedex, physical_packaging_fedex, weight, shipper_postal_code,shipper_country_code,customer_postal_code,customer_country_code, sys_default=False,cust_default=False, error=True, context=None):
        context = dict(self._context or {})
        if 'fedex_active' in context.keys() and context['fedex_active'] == False:
            return True
        shippingfedex_obj = self.env['shipping.fedex']
        shippingfedex_id = shippingfedex_obj.search([('active','=',True)])
        if not shippingfedex_id:
            if error:
                raise osv.except_osv(_('Error'), _('Default FedEx settings not defined'))
            else:
                return False
        else:
            shippingfedex_id = shippingfedex_id[0]

        shippingfedex_ptr = shippingfedex_id
        account_no = shippingfedex_ptr.account_no
        key = shippingfedex_ptr.key
        password = shippingfedex_ptr.password
        meter_no = shippingfedex_ptr.meter_no
        
        
        is_test = shippingfedex_ptr.test
        CONFIG_OBJ = FedexConfig(key=key, password=password, account_number=account_no, meter_number=meter_no, use_test_server=is_test)
        rate_request = FedexRateServiceRequest(CONFIG_OBJ)
        rate_request.RequestedShipment.DropoffType = dropoff_type_fedex
        rate_request.RequestedShipment.ServiceType = service_type_fedex
        rate_request.RequestedShipment.PackagingType = packaging_type_fedex
        rate_request.RequestedShipment.PackageDetail = package_detail_fedex
        rate_request.RequestedShipment.Shipper.Address.PostalCode = shipper_postal_code
        rate_request.RequestedShipment.Shipper.Address.CountryCode = shipper_country_code
        rate_request.RequestedShipment.Shipper.Address.Residential = False
        rate_request.RequestedShipment.Recipient.Address.PostalCode = customer_postal_code
        rate_request.RequestedShipment.Recipient.Address.CountryCode = customer_country_code
        rate_request.RequestedShipment.EdtRequestType = 'NONE'
        rate_request.RequestedShipment.ShippingChargesPayment.PaymentType = payment_type_fedex

        package1_weight = rate_request.create_wsdl_object_of_type('Weight')
        package1_weight.Value = weight
        package1_weight.Units = "LB"
        physical_packaging_fedex="BOX"
        package1 = rate_request.create_wsdl_object_of_type('RequestedPackageLineItem')
        package1.Weight = package1_weight
        #can be other values this is probably the most common
        package1.PhysicalPackaging = physical_packaging_fedex
        # Un-comment this to see the other variables you may set on a package.

        # This adds the RequestedPackageLineItem WSDL object to the rate_request. It
        # increments the package count and total weight of the rate_request for you.
        rate_request.add_package(package1)

        # If you'd like to see some documentation on the ship service WSDL, un-comment
        # this line. (Spammy).
        # Fires off the request, sets the 'response' attribute on the object.
#        try:
        rate_request.send_request()

#        except Exception, e:
#            if error:
#                raise Exception('%s' % (e))
#            return False

        # This will show the reply to your rate_request being sent. You can access the
        # Here is the overall end result of the query.

        for detail in rate_request.response.RateReplyDetails[0].RatedShipmentDetails:
            for surcharge in detail.ShipmentRateDetail.Surcharges:
                if surcharge.SurchargeType == 'OUT_OF_DELIVERY_AREA':
                    logger.info('ODA rate_request charge====> %s', surcharge.Amount.Amount)

        for rate_detail in rate_request.response.RateReplyDetails[0].RatedShipmentDetails:
            return rate_detail.ShipmentRateDetail.TotalNetFedExCharge.Amount
        
        
    shipping_type = fields.Selection(_get_shipping_type,'Shipping Type', default='All')
    
stock_picking()

class shipping_response(models.Model):
    _inherit = 'shipping.response'
    
    
    def generate_fedex_tracking_no(self, picking_id):
        '''
        This function is used to Generated FEDEX Shipping Label in Delivery order
        parameters: 
            picking : (int) stock picking ID,(delivery order ID)
        '''
        context = dict(self._context or {})
        shippingfedex_obj = self.env['shipping.fedex']
        stockpicking_obj = self.env['stock.picking']
        fedex_attachment_pool = self.env['ir.attachment']
        shippingfedex_id = shippingfedex_obj.search([('active','=',True)])
        if not shippingfedex_id:
            raise osv.except_osv(_('Error'), _('Default Fedex settings not defined'))
        else:
            shippingfedex_id = shippingfedex_id[0]
        reference = ''
        reference2 = ''
        count = 1
        sale_obj = self.env['sale.order']
        ss = sale_obj.browse(picking_id.sale_id.id)
        for move_line in picking_id.move_lines:
            reference += '('+str(int(move_line.product_qty))+')'
            if move_line.product_id.default_code:
                reference += str(move_line.product_id.default_code) + '+'
                if count > 4:
                    break
                count += 1
                
        reference = reference[:-1]
        reference = reference[30:]
        
        reference+= ' ' +shippingfedex_id.config_shipping_address_id.name
        shipper_address = shippingfedex_id.config_shipping_address_id
        
        
        if not shipper_address:
            raise osv.except_osv(_('Error'), _('Shipping Address not defined!'),)

        shipper = Address(shipper_address.name, shipper_address.street, shipper_address.street2 or '', shipper_address.city,  shipper_address.state_id.code or '', shipper_address.zip, shipper_address.country_id.code,  shipper_address.phone or '', shipper_address.email, shipper_address.name)

        ### Recipient
        cust_address = picking_id.partner_id
        receipient = Address(cust_address.name, cust_address.street, cust_address.street2 or '', cust_address.city, cust_address.state_id.code or '', cust_address.zip, cust_address.country_id.code, cust_address.phone or '', cust_address.email, cust_address.name)

        account_no = shippingfedex_id.account_no
        key = shippingfedex_id.key
        password = shippingfedex_id.password
        meter_no = shippingfedex_id.meter_no
        is_test = shippingfedex_id.test
        CONFIG_OBJ = FedexConfig(key=key, password=password, account_number=account_no, meter_number=meter_no, use_test_server=is_test)
        # This is the object that will be handling our tracking request.
        # We're using the FedexConfig object from example_config.py in this dir.
        shipment = FedexProcessShipmentRequest(CONFIG_OBJ)
        # This is very generalized, top-level information.
        # REGULAR_PICKUP, REQUEST_COURIER, DROP_BOX, BUSINESS_SERVICE_CENTER or STATION
        shipment.RequestedShipment.DropoffType = picking_id.dropoff_type_fedex #'REGULAR_PICKUP'
        # See page 355 in WS_ShipService.pdf for a full list. Here are the common ones:
        # STANDARD_OVERNIGHT, PRIORITY_OVERNIGHT, FEDEX_GROUND, FEDEX_EXPRESS_SAVER
        shipment.RequestedShipment.ServiceType = picking_id.service_type_fedex #'PRIORITY_OVERNIGHT'
        # What kind of package this will be shipped in.
        # FEDEX_BOX, FEDEX_PAK, FEDEX_TUBE, YOUR_PACKAGING
        shipment.RequestedShipment.PackagingType = picking_id.packaging_type_fedex  #'FEDEX_PAK'
        # No idea what this is.
        # INDIVIDUAL_PACKAGES, PACKAGE_GROUPS, PACKAGE_SUMMARY
        shipment.RequestedShipment.PackageDetail = picking_id.package_detail_fedex #'INDIVIDUAL_PACKAGES'
        # Shipper contact info.
        shipment.RequestedShipment.Shipper.Contact.PersonName = shipper.name #'Sender Name'
        shipment.RequestedShipment.Shipper.Contact.CompanyName = shipper.company_name #'Some Company'
        shipment.RequestedShipment.Shipper.Contact.PhoneNumber = shipper.phone #'9012638716'
        # Shipper address.
        address_rec_shipper = shipper.address1
        if shipper.address2:
            address_rec_shipper += "\n"+shipper.address2
        shipment.RequestedShipment.Shipper.Address.StreetLines = address_rec_shipper #['Address Line 1']
        shipment.RequestedShipment.Shipper.Address.City =  shipper.city #'Herndon'
        shipment.RequestedShipment.Shipper.Address.StateOrProvinceCode = shipper.state_code #'VA'
        shipment.RequestedShipment.Shipper.Address.PostalCode = shipper.zip #'20171'
        shipment.RequestedShipment.Shipper.Address.CountryCode = shipper.country_code #'US'
        shipment.RequestedShipment.Shipper.Address.Residential = False
        shipment.RequestedShipment.EdtRequestType = 'NONE'
        # Recipient contact info.
        shipment.RequestedShipment.Recipient.Contact.PersonName = receipient.name #'Recipient Name'
        shipment.RequestedShipment.Recipient.Contact.CompanyName = receipient.company_name #'Recipient Company'
        if receipient.phone:
            shipment.RequestedShipment.Recipient.Contact.PhoneNumber = receipient.phone #'9012637906'
        else:
            shipment.RequestedShipment.Recipient.Contact.PhoneNumber = shipper.phone #'9012637906'
        # Recipient address
        address_rec = receipient.address1

        if receipient.address2:
            address_rec += ','+receipient.address2

        shipment.RequestedShipment.Recipient.Address.StreetLines = address_rec #['Address Line 1']
        shipment.RequestedShipment.Recipient.Address.City = receipient.city #'Herndon'
        shipment.RequestedShipment.Recipient.Address.StateOrProvinceCode = receipient.state_code #'VA'
        shipment.RequestedShipment.Recipient.Address.PostalCode = receipient.zip #'20171'
        shipment.RequestedShipment.Recipient.Address.CountryCode = receipient.country_code #'US'
        # This is needed to ensure an accurate rate quote with the response.
        shipment.RequestedShipment.Recipient.Address.Residential = False
        # Who pays for the shipment?
        # RECIPIENT, SENDER or THIRD_PARTY
        shipment.RequestedShipment.ShippingChargesPayment.PaymentType = picking_id.payment_type_fedex #'SENDER'
#        shipment.RequestedShipment.ShippingChargesPayment.rate = picking_id.rate #'SENDER'
        # Specifies the label type to be returned.
        # LABEL_DATA_ONLY or COMMON2D
        shipment.RequestedShipment.LabelSpecification.LabelFormatType = 'COMMON2D'
        # Specifies which format the label file will be sent to you in.
        # DPL, EPL2, PDF, PNG, ZPLII
        shipment.RequestedShipment.LabelSpecification.ImageType = 'PNG'
        # To use doctab stocks, you must change ImageType above to one of the
        # label printer formats (ZPLII, EPL2, DPL).
        # See documentation for paper types, there quite a few.
        shipment.RequestedShipment.LabelSpecification.LabelStockType = 'PAPER_4X6'
        # This indicates if the top or bottom of the label comes out of the
        # printer first.
        # BOTTOM_EDGE_OF_TEXT_FIRST or TOP_EDGE_OF_TEXT_FIRST
        shipment.RequestedShipment.LabelSpecification.LabelPrintingOrientation = 'BOTTOM_EDGE_OF_TEXT_FIRST'
#            shipment.RequestedShipment.LabelSpecification.CustomerSpecifiedDetail.CustomContent.TextEntries = 'test'
        package1_weight = shipment.create_wsdl_object_of_type('Weight')
        # Weight, in pounds.
        package1_weight.Value = picking_id.weight_package #1.0
        package1_weight.Units = "LB"
        physical_packaging_fedex="BOX"
#        Dimension
        dimension = shipment.create_wsdl_object_of_type('Dimensions')
        dimension.Length = picking_id.length_package
        dimension.Width  = picking_id.width_package
        dimension.Height = picking_id.height_package
        dimension.Units  = 'IN'
        '''  Valid values are
        BILL_OF_LADING
        CUSTOMER_REFERENCE
        DEPARTMENT_NUMBER
        ELECTRONIC_PRODUCT_CODE
        INTRACOUNTRY_REGULATORY_REFERENCE
        INVOICE_NUMBER
        P_O_NUMBER
        SHIPMENT_INTEGRITY
        STORE_NUMBER  '''
        #Reference
        references = shipment.create_wsdl_object_of_type('CustomerReference')
        references.CustomerReferenceType = 'CUSTOMER_REFERENCE'
        references.Value = reference
        package1 = shipment.create_wsdl_object_of_type('RequestedPackageLineItem')
        package1.Weight = package1_weight
        package1.CustomerReferences = references
        package1.PhysicalPackaging = physical_packaging_fedex
        shipment.add_package(package1)
        try:
            shipment.send_request()
        except Exception, e:
            raise osv.except_osv(_('Error'), _('%s' % (e,)))
        # This will show the reply to your shipment being sent. You can access the
        # attributes through the response attribute on the request object. This is
        # good to un-comment to see the variables returned by the Fedex reply.
        # Here is the overall end result of the query.
#            raise osv.except_osv(_('Error'), _('%s' % (shipment.response,)))

        if shipment.response.HighestSeverity == 'ERROR':
            raise osv.except_osv(_('Error'), _('%s' % (shipment.response.Notifications[0].Message,)))
#        Getting the tracking number from the new shipment.
        fedexTrackingNumber = shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].TrackingIds[0].TrackingNumber
        # Get the label image in ASCII format from the reply. Note the list indices
        # we're using. You'll need to adjust or iterate through these if your shipment
        # has multiple packages.
        ascii_label_data = shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].Label.Parts[0].Image
#        ======================================
        im_barcode = cStringIO.StringIO(b64decode(ascii_label_data)) # constructs a StringIO holding the image
        img_barcode = Image.open(im_barcode)
        output = StringIO.StringIO()
        img_barcode.save(output, format='PNG')
        data = binascii.b2a_base64(output.getvalue())
        f = open('/tmp/test_fedex.png', 'wb')
        f.write(output.getvalue())
        f.close()
        #=======================
        #=======================
        c = canvas.Canvas("/tmp/picking_list_fedex.pdf")
        c.setPageSize((400, 650))
        c.drawImage('/tmp/test_fedex.png',10,10,380,630)
        c.save()
        f = open('/tmp/picking_list_fedex.pdf', 'rb')
        #=======================
#        ======================================
        fedex_data_attach = {
            'name': 'PackingList.pdf', 
            'datas': base64.b64encode(f.read()),
            'description': 'Packing List',
            'res_name': picking_id.name,
            'res_model': 'stock.picking',
            'res_id': picking_id.id,
        }
        fedex_attach_id = fedex_attachment_pool.search([('res_id','=',picking_id.id),('res_name','=',picking_id.name)])
        if not fedex_attach_id:
            fedex_attach_id = fedex_attachment_pool.create(fedex_data_attach)
            os.remove('/tmp/test_fedex.png')
            os.remove('/tmp/picking_list_fedex.pdf')
        else:
            fedex_attach_result = fedex_attach_id.write(fedex_data_attach)
            fedex_attach_id = fedex_attach_id[0]
        context['attach_id'] = fedex_attach_id
        context['tracking_no'] = fedexTrackingNumber
        if fedexTrackingNumber:
            stockpickingwrite_result = picking_id.write({'carrier_tracking_ref':fedexTrackingNumber, 'shipping_label':binascii.b2a_base64(str(b64decode(ascii_label_data)))})
            context['track_success'] = True
            ss.write({'client_order_ref':fedexTrackingNumber})
        return True
    
shipping_response()