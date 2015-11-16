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

from openerp.osv import osv
from openerp.tools.translate import _
import cStringIO
from datetime import datetime
import random
import StringIO
import time
import base64
from base64 import b64decode
from PyPDF2 import PdfFileMerger, PdfFileReader
from openerp import models, fields, api, _
import binascii
import commands
import os


class generate_label_pdf(models.TransientModel):
    _name = "generate.label.pdf"
    _description = "Generate Label PDF"
     

    def print_lable(self, cr, uid, ids, context={}):
        picking_object = self.pool.get('stock.picking')
        para = self.pool.get("ir.config_parameter")
        attachment_pool = self.pool.get('ir.attachment')
        ip_address = para.get_param(cr, uid, "web.base.url", context=context)
        dir_loc = os.path.dirname(os.path.abspath(__file__))
        a= dir_loc.split('/')
        a.pop()
        path = ""
        for i in a:
            if i == '':
                path = ""
            path += i + '/'
        new_path = path + 'static/src/'
        random_sequence = random.sample(range(1,1000),1)
        batch_file =  str(new_path) + '/sevicelabel' + str(random_sequence[0]) + '.pdf'
        
        if os.path.exists(batch_file):
            os.remove(batch_file)
        
        merger = PdfFileMerger()
        i = datetime.now()
        date = i.strftime('%Y/%m/%d %H:%M:%S')
        for pick in picking_object.browse(cr, uid, context.get('active_ids')):
            attachment_ids = attachment_pool.search(cr,uid,[('res_id','=',pick.id)])
            if attachment_ids:
                for i in attachment_ids:
                    a_obj = attachment_pool.browse(cr, uid, i)
                    file1 = new_path +str(pick.id)+".pdf"
                    f = open(file1, 'wb')
                    f.write(b64decode(a_obj.datas))
                    f.close()
                    merger.append(PdfFileReader(file(file1, 'rb')))
                picking_object.write(cr, uid, [pick.id], {'label_printed' : True, 'label_printed_datetime' : date})
        merger.write(str(batch_file))
        cr.commit()
        if attachment_ids:
            url =  ip_address + "/base_module_shipping/static/src" + '/sevicelabel' + str(random_sequence[0]) + '.pdf'
            return {
                            'type': 'ir.actions.act_url',
                            'url': url,
                            'target': 'new'
                    }
        if not attachment_ids:
           raise osv.except_osv(_('Error'), _('No Attachment Found!'),)

generate_label_pdf()