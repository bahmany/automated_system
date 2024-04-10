import os
from datetime import datetime
from io import BytesIO

import barcode
import img2pdf
from PIL import Image, ImageFont, ImageDraw
from barcode.writer import ImageWriter
from mongoengine import Q
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amsp.settings import BASE_DIR
from amspApp.Material.hamkaran_connect import get_PosPart, get_InvMUnit, get_InvvwPartType, get_InvAccCtgry, \
    get_NewPartID, insert_Hamkaran, get_PartInstance_By_PartNo, set_Location_To_PartNo, get_Anbar_Of_PartCode, \
    delete_partcode_from_mahale, get_PartInstanceComplete_By_PartCode, get_AccDLs
from amspApp.Material.models import MaterialLocations, Barcodes, MaterialHamkaranTafzil
from amspApp.Material.serializers.WarehouseSerializer import MaterialLocationsSerializer, BarcodesSerializer, \
    MaterialHamkaranTafzilSerializer
from amspApp.Notifications.views.NotificationView import NotificationViewSet
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class WarehousesViewSet(viewsets.ModelViewSet):

    # def checkPerm(self, req):
    #     if req.user.groups.filter(
    #             Q(name__contains="group_namayendgi_8_ostan")).count() > 0:
    #         raise Exception("مجوز دسترسی ندارید")

    # def initialize_request(self, request, *args, **kwargs):
    #     self.checkPerm(request)
    #     return super(WarehousesViewSet, self).initialize_request(request, *args, **kwargs)

    @detail_route(methods=["delete"])
    def deletebarcode(self, request, *args, **kwargs):
        id = kwargs['id']
        ss = Barcodes.objects.get(barcode=id)
        dt = {
            'position': 6322344
        }
        ss = BarcodesSerializer(instance=ss, data=dt, partial=True)
        ss.is_valid(raise_exception=True)
        ss.save()

        pp = NotificationViewSet()
        pp.send_to_group_message_with_ws(32424246, ss.data['barcode'], 'group_material', {
            'body': 'بارکد %s حذف شد' % (ss.data['barcode'],),
            'alarm': 'al_danger'
        })

        return Response({'result': 'ok'})

    @detail_route(methods=["get"])
    def get_location(self, request, *args, **kwargs):
        id = kwargs['id']
        ss = MaterialLocations.objects.get(id=id)
        ss = MaterialLocationsSerializer(instance=ss).data
        return Response(ss)

    @detail_route(methods=["get"])
    def good_stay_in_location(self, request, *args, **kwargs):
        id = kwargs['id']
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        ses = Barcodes.objects.get(Q(barcode=id), Q(position=87976544),
                                   (Q(confirmLocation=None) | Q(confirmLocation=False)))
        desc = ses.desc
        desc['good_stay_in_location_position_id'] = posiIns.positionID
        # sendGotify.delay(request.user.id, 'title', 'details', 5)
        data = {
            'id': ses.id,
            'confirmLocation': True,
            'confirmTime': datetime.now(),
            'desc': desc

        }
        ss = BarcodesSerializer(
            ses,
            data=data, partial=True)
        ss.is_valid(raise_exception=True)
        ss.save()
        dt = ss.data
        ss = NotificationViewSet()
        ss.send_to_group_message_with_ws(123121234, str(ses.id), 'group_material', {
            'body': 'کویل %s با وزن خاصل %s توسط باسکول در محل قرار گرفت' % (
                dt['desc']['product']['Name'] + ' ' + dt['desc']['product']['Code'],
                dt['desc']['barcode']['vazne_khales']),
            'alarm': 'al_succ'
        })
        return Response({'result': 'ok'})

    @detail_route(methods=["get"])
    def good_stay_in_location_with_QC_argue(self, request, *args, **kwargs):
        id = kwargs['id']
        ses = Barcodes.objects.get(Q(barcode=id), Q(position=87976544),
                                   (Q(confirmLocation=None) | Q(confirmLocation=False)))
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)

        desc = ses.desc
        desc['good_stay_in_location_position_id'] = posiIns.positionID

        # sendGotify.delay(request.user.id, 'title', 'details', 5)
        data = {
            'id': ses.id,
            'confirmLocation': True,
            'confirmTime': datetime.now(),
            'desc': desc,
            'position': 8845344,

        }
        ss = BarcodesSerializer(
            ses,
            data=data, partial=True)
        ss.is_valid(raise_exception=True)
        ss.save()
        dt = ss.data
        ss = NotificationViewSet()
        ss.send_to_group_message_with_ws(8974532, str(ses.id), 'group_material', {
            'body': 'کویل %s با وزن خاصل %s دارای مسائل کیفیتی است ولی در محل قرار گرفت' % (
                dt['desc']['product']['Name'], dt['desc']['barcode']['vazne_khales']),
            'alarm': 'al_warning'})
        return Response({'result': 'ok'})

    @detail_route(methods=["get"])
    def good_moved_another_location_with_QC_argue(self, request, *args, **kwargs):
        id = kwargs['id']
        ses = Barcodes.objects.get((Q(confirmLocation=None) |
                                    Q(confirmLocation=False))
                                   & Q(position=87976544) &
                                   Q(barcode=id)
                                   )
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)

        desc = ses.desc
        desc['good_stay_in_location_position_id'] = posiIns.positionID

        # sendGotify.delay(request.user.id, 'title', 'details', 5)
        data = {
            'id': ses.id,
            'confirmLocation': True,
            'confirmTime': datetime.now(),
            'desc': desc,
            'position': 7463333,
        }
        ss = BarcodesSerializer(
            ses,
            data=data, partial=True)
        ss.is_valid(raise_exception=True)
        ss.save()
        dt = ss.data
        ss = NotificationViewSet()
        ss.send_to_group_message_with_ws(643242, str(ses.id), 'group_material', {
            'body': 'کویل %s به وزن %s به انبار قرنطینه منتقل شد' % (
                dt['desc']['product']['Name'] + ' ' + dt['desc']['product']['Code'],
                dt['desc']['barcode']['vazne_khales']),
            'alarm': 'al_danger'
        })
        return Response({'result': 'ok'})

    @list_route(methods=["get"])
    def get_accdls(self, request, *args, **kwargs):
        result = get_AccDLs(request.query_params.get('q', ''))
        return Response(result)

    @list_route(methods=["post"])
    def post_shelf(self, request, *args, **kwargs):
        dt = {
            'name': request.data['name'],
            'x': request.data['x'],
            'y': request.data['y'],
            'z': request.data['z'],
        }
        if (request.data.get('id')):
            ins = MaterialLocations.objects.get(id=request.data.get('id'))
            ser = MaterialLocationsSerializer(data=dt, instance=ins, partial=True)
            ser.is_valid(raise_exception=True)
            ser.save()
            return Response({'resilt': 'ok'})
        ser = MaterialLocationsSerializer(data=dt)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({'resilt': 'ok'})

    @list_route(methods=['get'])
    def get_material_hamkaran_tafzil_list(self, request, *args, **kwargs):
        lst = MaterialHamkaranTafzil.objects.all()
        lst = MaterialHamkaranTafzilSerializer(instance=lst, many=True).data
        return Response(lst)

    @list_route(methods=['post'])
    def update_material_hamkaran_tafzil(self, request, *args, **kwargs):
        dt = request.data
        ser = None
        if dt.get(id):
            inst = MaterialHamkaranTafzil.objects.get(id=dt['id'])
            ser = MaterialHamkaranTafzilSerializer(instance=inst, data=dt, partial=True)
            ser.is_valid(raise_exception=True)
            ser = ser.save()
        else:
            ser = MaterialHamkaranTafzilSerializer(data=dt)
            ser.is_valid(raise_exception=True)
            ser = ser.save()
        ser = MaterialHamkaranTafzilSerializer(instance=ser).data
        return Response(ser)

    @list_route(methods=['post'])
    def delete_material_hamkaran_tafzil(self, request, *args, **kwargs):
        MaterialHamkaranTafzil.objects.get(id=request.data['id']).delete()
        return Response({})

    @list_route(methods=['get'])
    def get_InvMUnit(self, request, *args, **kwargs):
        units = get_InvMUnit()
        return Response(units)

    @list_route(methods=['get'])
    def get_InvvwPartType(self, request, *args, **kwargs):
        units = get_InvvwPartType()
        return Response(units)

    @list_route(methods=['get'])
    def get_InvAccCtgry(self, request, *args, **kwargs):
        units = get_InvAccCtgry()
        return Response(units)

    # @list_route(methods=["get"])
    # def get_vendors(self, request, *args, **kwargs):
    #     return Response(get_vendors())

    """
    # @list_route(methods=['post'])
    # def tmp_create_barcode(self, request, *args, **kwargs):
    #     odoo = connectToOdoo()
    #     uid = odoo.connect()
    #     product_id_of_odoo = get_product_from_hamkaran_serial(request.data['product']['Serial'])
    #     # here we must create purchase in odoo
    #     dt = dict(
    #         partner_id=request.data['barcode']['sherkate_sazandeh'],  # vendor ID
    #         order_line=([0, 0, dict(
    #             name=str(product_id_of_odoo['product_variant_ids'][0]),
    #             product_id=product_id_of_odoo['product_variant_ids'][0],
    #             date_planned=datetime.now(),
    #             product_qty=request.data['barcode']['vazne_khales'],
    #             product_uom=product_id_of_odoo['uom_id'][0],
    #             price_unit=0,
    #         )],)
    #     )
    #
    #     purchaseID = odoo.write(uid=uid,
    #                             model='purchase.order', action="create", data=[dt])
    #
    #     button_confirm = odoo.write(uid=uid,
    #                                 model='purchase.order', action="button_confirm", data=(purchaseID,))
    #
    #     action_view_picking = odoo.write(uid=uid,
    #                                      model='purchase.order', action="action_view_picking", data=(purchaseID,))
    #
    #     resultOfInv = odoo.write(uid=uid,
    #                             model='stock.move', action="write", data=[dt])
    #     res_id = resultOfInv['res_id']
    #
    #     # setting serial and lots and packing
    #
    #
    #     # button_confirm = odoo.write(uid=uid,
    #     #                             model='purchase.order', action="button_confirm", data=(purchaseID,))
    #
    #
    #
    #     # action_view_picking = odoo.write(uid=uid,
    #     #                                  model='purchase.order', action="action_view_picking", data=(purchaseID,))
    #
    #     # action_view_picking = odoo.write(uid=uid,
    #     #                                  model='stock.picking', action="load_views", data=dict(
    #     #         active_id=purchaseID,
    #     #         active_ids=[purchaseID],
    #     #         active_model="purchase.order",
    #     #         params={'action': 301}
    #     #
    """

    @detail_route(methods=['get'])
    def listBarcodeBy_xyz(self, request, *args, **kwargs):
        locationLink = kwargs['id']
        barcodes = Barcodes.objects.filter(
            locationLink=locationLink,
            position__in=[87976544, 8845344]
        )
        bss = BarcodesSerializer(instance=barcodes, many=True).data

        return Response(bss)

    @list_route(methods=['post'])
    def get_barcode_by_location(self, request, *args, **kwargs):
        dt = {
            "x": request.data['location']['x'],
            "y": request.data['location']['y'],
            "z": request.data['location']['z'],
            'locationLink': request.data['currentLocation']['id'],
            'position__in': [87976544, 8845344]
        }
        barcode = Barcodes.objects.filter(**dt)
        if barcode.count() != 0:
            barcode = barcode.first()
            bs = BarcodesSerializer(instance=barcode).data
            return Response(bs)

        return Response({})

    @list_route(methods=['post'])
    def block_location(self, request, *args, **kwargs):
        pass

    @list_route(methods=['post'])
    def create_barcode(self, request, *args, **kwargs):
        dt = {
            "desc": request.data,
            "x": request.data['location']['x'],
            "y": request.data['location']['y'],
            "z": request.data['location']['z'],
            'locationLink': request.data['currentLocation']['id'],
            'position': 87976544
        }
        # wareIns = MaterialLocations.objects.get(id = request.data['currentLocation']['id'])
        # wareIns = MaterialLocationsSerializer(instance=wareIns).data
        duplicated = Barcodes.objects.filter(
            x=request.data['location']['x'],
            y=request.data['location']['y'],
            z=request.data['location']['z'],
            locationLink=request.data['currentLocation']['id'],
            position=87976544).count()
        if duplicated > 0:
            raise Exception('this position is full ')

        mybarcode = datetime.now().strftime("%y%m%d%H%M%S%f")
        dt['barcode'] = mybarcode
        if dt.get('desc', {}).get('product', {}).get('Version', None) is not None:
            del dt['desc']['product']['Version']
        # dt['desc'] = mybarcode
        sr = BarcodesSerializer(data=dt)
        sr.is_valid(raise_exception=True)
        sr = sr.save()

        rv = BytesIO()
        EAN = barcode.get('code128', code=str(mybarcode), writer=ImageWriter(),
                          writer_options={'text_distance': 0, 'text_line_distance': 0})
        EAN.write(rv)
        barcode_image = Image.open(rv)
        barcode_image_size = barcode_image.size
        # im1 = im.crop((left, top, right, bottom))
        finalBarcode = barcode_image.crop((0, 30, barcode_image_size[0], barcode_image_size[1] - 150))

        result_size = (2268, 1559)
        img = Image.new('RGB', result_size, 'white')

        # merging barcode into img
        (width, height) = finalBarcode.size
        sampler = result_size[0] / width
        height1 = int(height * float(sampler))
        result = finalBarcode.resize((result_size[0], height1), Image.ANTIALIAS)
        img.paste(im=result, box=(0, 30))

        # drawing ----------------------------
        fontsize = 75
        font = ImageFont.truetype(BASE_DIR + "/amspApp/static/fonts/centurygothic_ufont.ir-webfont.ttf", fontsize, )
        draw = ImageDraw.Draw(img)

        draw.text((90, height1 + 20), mybarcode + " - Weighbridge", (0, 0, 0),
                  font=font)  # this will draw text with Blackcolor and 16 size
        draw.rectangle(((0, height1 + 120), (2268, height1 + 590)), (0, 0, 0))
        newFont = ImageFont.truetype(BASE_DIR + "/amspApp/static/fonts/centurygothic_ufont.ir-webfont.ttf", 355, )

        draw.text((90, height1 + 120), " LOC : " + request.data['location']['locationTitle'] + " ", (255, 255, 255),
                  font=newFont)  # this will draw text with Blackcolor and 16 size
        # draw.text((90, height1 + 120),
        #           request.data['location']['locationTitle'])  # this will draw text with Blackcolor and 16 size
        height1 = height1 + 360
        draw.text((90, height1 + 220), "Date Post : %s" % (sr.dateOfPost.strftime("%Y/%m/%d %H:%M:%S")), (0, 0, 0),
                  font=font)  # this will draw text with Blackcolor and 16 size
        draw.text((90, height1 + 310), "Date Enter : %s" % (sr.desc['barcode']['dateOf']), (0, 0, 0),
                  font=font)  # this will draw text with Blackcolor and 16 size
        draw.text((90, height1 + 400), "Net Weight : %d" % (sr.desc['barcode']['vazne_khales']), (0, 0, 0),
                  font=font)  # this will draw text with Blackcolor and 16 size
        draw.text((90, height1 + 500),
                  "PartCode : %s" % (sr.desc['product']['Code']),
                  (0, 0, 0), font=font)  # this will draw text with Blackcolor and 16 size

        final = BytesIO()
        img.save(final, format='JPEG')
        image_data = final.getvalue()

        """
        label size : 5.5cm x 8.0cm
                    2268 x 1559 pixel
        """

        pdf = img2pdf.convert(image_data)
        f = os.path.abspath(os.path.join(BASE_DIR, "amspApp/static/barcodes/" + mybarcode + ".pdf"))

        f = open(f, 'wb')
        f.write(pdf)
        f.close()
        url = "/static/barcodes/" + mybarcode + ".pdf"

        # response = HttpResponse(pdf, content_type="application/pdf")
        # response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

        pp = NotificationViewSet()
        pp.send_to_group_message_with_ws(7, dt['barcode'], 'group_material', {
            'body': 'کویل %s با وزن خاصل %s توسط باسکول رسید شد' % (
                dt['desc']['product']['Name'] + ' ' + dt['desc']['product']['Code'],
                dt['desc']['barcode']['vazne_khales']),
            'alarm': 'al_succ'
        })

        return Response({'url': url})

        # return Response(BarcodesSerializer(instance=sr).data)

    @detail_route(methods=['post'])
    def taeed_vazn(self, request, *args, **kwargs):
        ins = Barcodes.objects.get(barcode=kwargs['id'])
        dt = ins['desc']
        dt['barcode']['vazne_khales'] = request.data['vazn']
        dt['barcode']['confirm_vazn'] = True
        if type(request.data['vazn']) != int:
            raise Exception('Enter Number please')
        ser = BarcodesSerializer(instance=ins, data={
            'desc': dt
        }, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({"result": "ok"})

    @list_route(methods=['post'])
    def post_part(self, request, *args, **kwargs):
        json = request.data
        """
        اول باید یک آی دی جدید دریافت کنیم
        """
        newID = get_NewPartID()[0]
        """
        
        """
        json['Serial'] = newID['NewID']
        insert = insert_Hamkaran(json)
        pins = get_PartInstanceComplete_By_PartCode(json['PartCode'])[0]
        return Response({"result": "ok", "posted_data": pins})

    @list_route(methods=['get'])
    def get_anbars_of_reg(self, request, *args, **kwargs):
        params = request.query_params
        anbars = get_Anbar_Of_PartCode(params.get('q'))
        return Response(anbars)

    @list_route(methods=['post'])
    def delete_anbars_of_reg(self, request, *args, **kwargs):
        data = request.data
        result = delete_partcode_from_mahale(data['PosPartRef'], data['PartRef'])

        return Response({"result": "ok"})

    @list_route(methods=['get'])
    def get_anbars(self, request, *args, **kwargs):
        anbars = get_PosPart()

        # best recursove tree maker
        # def rec(query, parent):
        #     parent['children'] = []
        #     for item in query:
        #         if item['Parent'] == parent['Serial']:
        #             parent['children'].append(item)
        #             rec(query, item)

        # root = {'Serial': None}
        # rec(anbars, root)
        # return Response(root['children'])
        return Response(anbars)

    @list_route(methods=["get"])
    def list_warehouses(self, request, *args, **kwargs):
        lst = MaterialLocations.objects.all()
        lst = MaterialLocationsSerializer(instance=lst, many=True).data
        return Response(lst)
        # odoo = connectToOdoo()
        # uid = odoo.connect()
        # result = odoo.search(uid=uid,
        #                      model='stock.warehouse',
        #                      action='search_read',
        #                      queries=[[]],
        #                      parameters={'limit': 99999}
        #                      )
        # result = list(result)
        # for r in result:
        #     cc = OdooWarehouses.objects.filter(linkToOdoo=r['id'])
        #     if cc.count() == 0:
        #         dt = {
        #             'linkToOdoo': r['id'],
        #             'x': 0,
        #             'y': 0,
        #             'z': 0,
        #             'desc': {},
        #         }
        #         ser = OdooWarehousesSerializer(data=dt)
        #         ser.is_valid(raise_exception=True)
        #         ser.save()
        #
        # for r in result:
        #     cc = OdooWarehouses.objects.filter(linkToOdoo=r['id']).first()
        #     r['x'] = cc.x
        #     r['y'] = cc.y
        #     r['z'] = cc.z
        #     r['desc'] = cc.desc

        # return Response({})

    @list_route(methods=['post'])
    def post_location(self, request, *args, **kwargs):
        data = request.data
        dt = {
            'Serial': data['part']['Serial'],
            'PosPartRef': data['node']['Serial'],
            'Active': 1
        }

        set_Location_To_PartNo(dt)

        return Response({"result": "ok"})

    @list_route(methods=['post'])
    def get_PartInstance_By_PartNo(self, request, *args, **kwargs):
        partno = request.data['partno']
        result = get_PartInstance_By_PartNo(partno)
        if (len(result) > 0):
            rr = result[0]
            rr['UseForBascul'] = bool(rr.get('UseForBascul'))
            rr['DisActive'] = not bool(rr.get('DisActive'))
            return Response(rr)
        return Response({'partno': partno})
