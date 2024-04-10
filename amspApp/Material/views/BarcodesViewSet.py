from datetime import datetime

import bson
from asq.initiators import query
from mongoengine import Q
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh, mil_to_sh_with_time, sh_to_mil
from amspApp.Material.hamkaran_connect import get_VchHdrIDFromVchNum
from amspApp.Material.models import Barcodes, MaterialTolidOrderItems, MaterialTolidOrder
from amspApp.Material.serializers.WarehouseSerializer import BarcodesSerializer, MaterialTolidOrderSerializer, \
    MaterialTolidIOrdertemsSerializer
from amspApp.Notifications.serializers.NotificationSerializer import NotificationsSerializer
from amspApp.Notifications.views.NotificationView import NotificationViewSet
from amspApp._Share.ListPagination import DataTableForNewDatables_net, DataTableForNewDatablesForAgg_post
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage


class BarcodesViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Barcodes.objects.all().filter(position__ne=6322344).order_by('-id')
    serializer_class = BarcodesSerializer

    # pagination_class = DataTablesPagination

    pagination_class = DataTableForNewDatables_net
    dtcold = [
        {'type': "string", 'data': 'barcode', 'title': 'شماره بارکد'},
        {'type': "string", 'data': 'desc.currentLocation.name', 'title': 'نام انبار'},
        {'type': "num-fmt", 'data': 'x', 'title': 'x'},
        {'type': "num-fmt", 'data': 'y', 'title': 'y'},
        {'type': "num-fmt", 'data': 'z', 'title': 'z'},
        {'type': "string", 'data': 'confirmLocation', 'title': 'تایید نشست'},
        {'type': "string", 'data': 'desc.barcode.confirm_vazn', 'title': 'تایید وزن'},
        {'type': "string", 'data': 'desc.barcode.dateOf', 'title': 'تاریخ ورود'},
        {'type': "string", 'data': 'desc.barcode.accdl.Title', 'title': 'سازنده'},
        {'type': "string", 'data': 'desc.barcode.accdl.AccNum', 'title': 'کد سازنده'},
        {'type': "string", 'data': 'desc.barcode.size_varagh', 'title': 'سایز'},
        {'type': "string", 'data': 'desc.barcode.vazne_khales', 'title': 'وزن خالص ادعایی'},
        {'type': "string", 'data': 'desc.barcode.shomare_kalaf', 'title': 'شماره کلاف'},
        {'type': "string", 'data': 'hamkaranSanad', 'title': 'همکاران'},
    ]

    pagination_class.dtcols = dtcold

    def retrieve(self, request, *args, **kwargs):
        if not bson.objectid.ObjectId.is_valid(kwargs.get("id")):
            barcode_ins = Barcodes.objects.filter(barcode=kwargs.get("id")).first()
            if barcode_ins is not None:
                serializer = self.get_serializer(barcode_ins)
                return Response(serializer.data)

        return super(BarcodesViewSet, self).retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        result = super(BarcodesViewSet, self).list(request, *args, **kwargs)
        for r in result.data['data']:
            if r['desc'].get('barcode'):
                if r['desc']['barcode'].get('confirm_vazn') is None:
                    r['desc']['barcode']['confirm_vazn'] = False
                if r['desc']['barcode'].get('accdl') == None:
                    r['desc']['barcode']['accdl'] = {}
                    r['desc']['barcode']['accdl']['Title'] = None
                    r['desc']['barcode']['accdl']['AccNum'] = None
                    r['desc']['barcode']['size_varagh'] = None
                    r['desc']['barcode']['vazne_khales'] = None
                    r['desc']['barcode']['shomare_kalaf'] = None

        return result

    @list_route(methods=['post'])
    def postqcbp(self, request, *args, **kwargs):
        dt = request.data['desc']
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        dt['postqcbp_positionid'] = posiIns.positionID
        dt['postqcbp_dateOfPost'] = datetime.now()
        defIns = self.queryset.get(id=request.data['id'])
        ser = self.serializer_class(instance=defIns, data={'desc': dt}, partial=True)
        ser.is_valid(raise_exception=True)
        ser = ser.save()
        return Response(self.serializer_class(instance=ser).data)

    @list_route(methods=['post'])
    def convertToScrap(self, request, *args, **kwargs):
        dt = request.data['desc']
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        dt['convertToScrap_positionid'] = posiIns.positionID
        dt['convertToScrap_dateOfPost'] = datetime.now()
        defIns = self.queryset.get(id=request.data['id'])
        ser = self.serializer_class(instance=defIns, data={'desc': dt}, partial=True)
        ser.is_valid(raise_exception=True)
        ser = ser.save()
        ser2 = self.serializer_class(instance=defIns, data={'position': 6879789}, partial=True)
        ser2.is_valid(raise_exception=True)
        ser2 = ser2.save()

        return Response(self.serializer_class(instance=ser2).data)

    @list_route(methods=['get'])
    def getQCBLProblems(self, request, *args, **kwargs):

        self.queryset = self.queryset.filter(position__in=[8845344, 7463333], desc__ready_to_tolid__in=[None, False])
        result = self.serializer_class(instance=self.queryset, many=True).data
        return Response(result)

    @detail_route(methods=['get'])
    def getInstanceByBarcode(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @list_route(methods=['get'])
    def getDatatableCols(self, request, *args, **kwargs):
        for d in self.dtcold:
            if d.get('join'):
                del d['join']
            if d.get('join_model'):
                del d['join_model']
        return Response(self.dtcold)

    @list_route(methods=['get'])
    def send_test_ws(self, request, *args, **kwargs):
        redis_publisher = RedisPublisher(facility='foobar', users=['bahmany'])
        message = RedisMessage('Hello World')
        redis_publisher.publish_message(message)
        return Response({})

    @list_route(methods=['post'])
    def set_qc_claim(self, request, *args, **kwargs):
        positionType = request.data['tp']
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        positionType = 8845344 if positionType == 87976544 else 7463333
        dt = {
            'dateOfQC': datetime.now(),
            'positionID': posiIns.positionID
        }

        ser = self.queryset.get(id=request.data['dt']['id'])
        ser1 = self.serializer_class(instance=ser, data={
            'position': positionType
        }, partial=True)
        ser1.is_valid(raise_exception=True)
        ser1.save()

        ser = self.queryset.get(id=request.data['dt']['id'])
        dd = ser.desc
        dd['qc_not_confirm'] = dt

        ser1 = self.serializer_class(instance=ser, data={'desc': dd}, partial=True)
        ser1.is_valid(raise_exception=True)
        ser1.save()
        return Response({'msg': 'ok'})

    @list_route(methods=["get"])
    def list_unlocated_goods(self, request, *args, **kwargs):
        goods = Barcodes.objects.filter(
            (Q(confirmLocation=None) |
             Q(confirmLocation=False)) & Q(position=87976544)
        )
        # , position = 1, confirmLocation = False
        goods = BarcodesSerializer(instance=goods, many=True).data
        return Response(goods)

    @list_route(methods=['post'])
    def postHamkaranSanadNo(self, request, *args, **kwargs):
        dt = request.data
        ins = Barcodes.objects.get(id=dt['barcodeID'])
        dtt = ins.desc
        dtt['VchHdr'] = get_VchHdrIDFromVchNum(dt['hamkaranSanad'])[0]
        ser = BarcodesSerializer(instance=ins, data={
            'hamkaranSanad': dt['hamkaranSanad'],
            'desc': dtt
        }, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({'result': 'ok'})

    @detail_route(methods=['post'])
    def postmasraf(self, request, *args, **kwargs):
        ins = Barcodes.objects.get(id=kwargs['id'])
        dtt = ins['desc']
        request.data['VchHdr'] = get_VchHdrIDFromVchNum(request.data['hamkaranSanad'])[0]
        dtt['masraf'] = request.data

        dt = {
            'position': 6656336,
            'mizaneMasraf': request.data['mizan'],
            'desc': dtt
        }
        ser = BarcodesSerializer(instance=ins, data=dt, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({'result': 'ok'})

    dt = [
        {'type': "string", 'data': 'barcode', 'title': 'بارکد'},
        {'type': "num-fmt", 'data': 'x', 'title': 'x'},
        {'type': "num-fmt", 'data': 'y', 'title': 'y'},
        {'type': "num-fmt", 'data': 'z', 'title': 'z'},
        {'type': "string", 'data': 'partcode', 'title': 'کد'},
        {'type': "string", 'data': 'noe', 'title': 'نوع'},
        {'type': "string", 'data': 'keifiat', 'title': 'سازنده'},
        {'type': "string", 'data': 'temper', 'title': 'تمپر'},
        {'type': "string", 'data': 'sath', 'title': 'سطح'},
        {'type': "string", 'data': 'zekhamat', 'title': 'ضخامت'},
        {'type': "string", 'data': 'arz', 'title': 'عرض'},
        {'type': "string", 'data': 'darajeh', 'title': 'درجه'},
        {'type': "string", 'data': 'tool', 'title': 'طول'},
        {'type': "num-fmt", 'data': 'mizane_tolid', 'title': 'تولید شده'},
        {'type': "string", 'data': 'location', 'title': 'موقعیت'},
        {'type': "string", 'data': 'dateOfPost', 'title': 'ورود'},
        {'type': "num-fmt", 'data': 'hoursInAnbar', 'title': 'روز'},
        {'type': "num-fmt", 'data': 'vazneKhales', 'title': 'وزن خالص'},
        {'type': "num-fmt", 'data': 'sumOfTolid', 'title': 'مصرف شده'},
        {'type': "num-fmt", 'data': 'baghimandeh', 'title': 'باقیمانده'},
    ]

    @list_route(methods=['get'])
    def getBarcodeWithDetailsForBarnameRiziColumns(self, request, *args, **kwargs):

        return Response(self.dt)

    @list_route(methods=['post'])
    def getBarcodeWithDetailsForBarnameRizi(self, request, *args, **kwargs):
        today = datetime.now()

        defaultAggr_project = {
            '$project':
                {
                    'DT_RowData': {'pkey': '$_id'},
                    'DT_RowId': '$_id',
                    'barcode': 1,
                    'locationLink': 1,
                    'x': 1,
                    'y': 1,
                    'z': 1,
                    'partcode': '$desc.product.Code',
                    'noe': {'$substr': ['$desc.product.Code', 0, 2]},
                    'keifiat': {'$substr': ['$desc.product.Code', 2, 1]},
                    'temper': {'$substr': ['$desc.product.Code', 3, 1]},
                    'sath': {'$substr': ['$desc.product.Code', 4, 1]},
                    'zekhamat': {'$substr': ['$desc.product.Code', 5, 2]},
                    'arz': {'$substr': ['$desc.product.Code', 8, 3]},
                    'darajeh': {'$substr': ['$desc.product.Code', 10, 1]},
                    'tool': {'$substr': ['$desc.product.Code', 11, 3]},
                    'vazneKhales': '$desc.barcode.vazne_khales',
                    'mizane_tolid': {'$ifNull': ['$desc.mizane_tolid', 0]},
                    'location': '$desc.location.locationTitle',
                    'dateOfPost': 1,
                    'position': 1,
                    'desc': 1,
                    'hoursInAnbar': {
                        '$divide': [{'$subtract': [today, "$dateOfPost"]},
                                    24 * (60 * 60 * 1000)]
                    },
                    'tolid': "$tolid",
                }
        }

        dtt = DataTableForNewDatablesForAgg_post()

        dtt.dtcols = self.dt

        result = dtt.paginate_queryset(Barcodes.objects, defaultAggr_project, request)

        # items = list(items)
        # items = Response(items).data
        # df = pd.DataFrame.from_records(items, index=[0])
        for d in result['data']:
            d['dateOfPost'] = mil_to_sh_with_time(d['dateOfPost'])
            d['hoursInAnbar'] = int(d['hoursInAnbar'])

        labels = query(result['chart']).select(lambda x: x['_id']).order_by().to_list()
        series = ['Kg']
        data = query(result['chart']).select(lambda x: x['vazn']).to_list()
        result['chart_graph'] = {}
        result['chart_graph']['labels'] = labels
        result['chart_graph']['series'] = series
        result['chart_graph']['data'] = data

        labels = query(result['chart65']).select(lambda x: x['_id']).order_by().to_list()
        series = ['Kg']
        data = query(result['chart65']).select(lambda x: x['vazn']).to_list()
        result['chart_graph65'] = {}
        result['chart_graph65']['labels'] = labels
        result['chart_graph65']['series'] = series
        result['chart_graph65']['data'] = data

        labels = query(result['chart66']).select(lambda x: x['_id']).order_by().to_list()
        series = ['Kg']
        data = query(result['chart66']).select(lambda x: x['vazn']).to_list()
        result['chart_graph66'] = {}
        result['chart_graph66']['labels'] = labels
        result['chart_graph66']['series'] = series
        result['chart_graph66']['data'] = data

        return Response(result)

    @list_route(methods=['post'])
    def saveTolid(self, request, *args, **kwargs):
        basket = request.data
        # checking before save
        has_error = False
        for b in basket['items']:
            b['error'] = None
            instance = Barcodes.objects.get(id=b['_id'])
            vazn = Barcodes.objects.get(id=b['_id']).desc['barcode']['vazne_khales']
            tolid = b.get('mizane_tolid', 0)
            if vazn - tolid < 0:
                has_error = True
                b['error'] = [
                    'میزان تولید را اصلاح نمایید'
                ]
            if tolid == 0:
                has_error = True
                b['error'] = [
                    'مقداری را برای تولید وارد نمایید'
                ]

        # checking with Barcodes.desc.barcode.vazne_khales
        # ------------------------------------------------------------------------------------------------------
        cc = query(basket['items']).group_by(lambda x: x['barcode'],
                                             result_selector=lambda key, group: {'barcode': key,
                                                                                 'mizan': query(group).sum(
                                                                                     lambda y: y['ersal_be_tolid'])}
                                             ).to_list()
        instances = Barcodes.objects.filter(barcode__in=query(cc).select(lambda x: x['barcode']).to_list())
        has_error = False
        barcodes = []
        for ins in instances:
            checkins = query(cc).where(lambda x: x['barcode'] == ins.barcode).first()
            if checkins['mizan'] > ins.desc['barcode']['vazne_khales']:
                barcodes.append(ins.barcode)
                has_error = True
        if has_error:
            basket['calc_error'] = "جمع کویل هایی با بارکد یکسان از موجودی بیشتر است" + " " + " , ".join(barcodes)
            return Response({"error": basket})
        # ------------------------------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------------------------------
        # checking with MaterialTolidOrderItems
        barcodeIds = query(instances).select(lambda x: x.id).to_list()
        tolidInstances = MaterialTolidOrderItems.objects.filter(linkBarcode__in=barcodeIds)
        tolidFromAll = query(tolidInstances).group_by(lambda x: x.linkBarcode.barcode,
                                                      result_selector=lambda key, group: {
                                                          'id': key,
                                                          'sumOfTolif': query(group).sum(lambda x: x.mizaneMasraf)
                                                      }
                                                      ).to_list()

        cc = query(basket['items']).group_by(lambda x: x['barcode'],
                                             result_selector=lambda key, group: {'barcode': key,
                                                                                 'mizan': query(group).sum(
                                                                                     lambda y: y['ersal_be_tolid'])}
                                             ).to_list()
        has_error = False
        barcodes = []
        for t in tolidFromAll:
            checkins = query(cc).where(lambda x: x['barcode'] == t['id']).first()
            barcodeInstance = Barcodes.objects.get(barcode=checkins['barcode'])
            vazne_khales = barcodeInstance.desc['barcode']['vazne_khales']
            if checkins['mizan'] > (vazne_khales - t['sumOfTolif']):
                has_error = True
                barcodes.append(checkins['barcode'])

        if has_error:
            basket['calc_error'] = "جمع کویل هایی با بارکد یکسان از موجودی بیشتر است" + " " + " , ".join(barcodes)
            return Response({"error": basket})
        # ------------------------------------------------------------------------------------------------------

        mildate = ''
        currentPos = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        forDate = datetime.strptime(sh_to_mil(request.data['forDate'], has_time=True), "%Y/%m/%d %H:%M:%S")
        newOrder = {
            "dateOfPost": datetime.now(),
            "forDate": datetime.now(),
            "positionID": currentPos.positionID,
            "desc": {'files': basket.get('files', [])}
        }
        mt = MaterialTolidOrderSerializer(data=newOrder)
        mt.is_valid(raise_exception=True)
        tolidInstance = mt.save()
        forNoti = []
        for b in basket['items']:
            barcode_instance = Barcodes.objects.get(barcode=b['barcode'])
            dt = {
                "dateOfPost": datetime.now(),
                "positionID": currentPos.positionID,
                "linkMaterialTolid": tolidInstance.id,
                "linkBarcode": barcode_instance.id,
                "mizaneMasraf": b['ersal_be_tolid'],
                "desc": {}
            }
            dis = MaterialTolidIOrdertemsSerializer(data=dt)
            dis.is_valid(raise_exception=True)
            dis = dis.save()
            forNoti.append(MaterialTolidIOrdertemsSerializer(instance=dis).data)

        # -----------------------------------------------------------------------------------------------------
        # after this we must send notification
        pp = NotificationViewSet()

        # ss.send_to_group_message_with_ws(5, str(ses.id), 'group_material', {
        #     'body': 'کویل %s با وزن خاصل %s دارای مسائل کیفیتی است ولی در محل قرار گرفت' % (
        #         dt['desc']['product']['PartName'] + ' ' + dt['desc']['product']['PartCode'],
        #         dt['desc']['barcode']['vazne_khales']),
        #     'alarm': 'al_warning'})

        pp.send_to_group_message_with_ws(54345634, 'صدور برنامه تولید', 'group_material', {
            'body':
                'برنامه تولید جدیدی ایجاد شد با جمع کل %d کیلو ایجاد شد' % (
                    query(forNoti).sum(lambda x: x['mizaneMasraf'])),
            'alarm': 'al_succ'
        })

        return Response({})

    @list_route(methods=['get'])
    def getMaterialForTolid(self, request, *args, **kwargs):
        mtos = MaterialTolidOrder.objects.filter(desc__done=None).order_by('forDate')
        mtos = MaterialTolidOrderSerializer(instance=mtos, many=True).data
        for m in mtos:
            mtoi = MaterialTolidOrderItems.objects.filter(linkMaterialTolid=m['id'])
            mtoi = MaterialTolidIOrdertemsSerializer(instance=mtoi, many=True).data
            m['items'] = mtoi
        return Response(mtos)

    @list_route(methods=['post'])
    def getToTolid(self, request, *args, **kwargs):
        currentPos = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        tolidInstance = MaterialTolidOrder.objects.get(id=request.data['barname']['id'])
        tolidItem = MaterialTolidOrderItems.objects.get(
            linkMaterialTolid=tolidInstance.id,
            id=request.data['coil']['id']
        )
        desc = tolidItem.desc
        desc['done'] = True
        desc["done_date"] = datetime.now()
        desc['done_positionID'] = currentPos.positionID
        msi = MaterialTolidIOrdertemsSerializer(instance=tolidItem, data={"desc": desc}, partial=True)
        msi.is_valid(raise_exception=True)
        msi = msi.save()
        barcodeInstance = Barcodes.objects.get(id=request.data['coil']['linkBarcode']['id'])
        dt = {
            'position': 6656336,
            'desc': barcodeInstance.desc
        }
        dt['desc']['masraf_datetime'] = datetime.now()
        dt['desc']['masraf_positionID'] = currentPos.positionID
        bs = BarcodesSerializer(instance=barcodeInstance, data=dt, partial=True)
        bs.is_valid(raise_exception=True)
        bs = bs.save()

        # checking if all items done the we done MaterialTolidOrder
        itemsNotFinished = MaterialTolidOrderItems.objects.filter(
            desc__done=None,
            linkMaterialTolid=tolidInstance.id
        ).count()
        if itemsNotFinished == 0:
            dt = tolidInstance.desc
            dt['done'] = True
            dt["done_date"] = datetime.now()
            dt['done_positionID'] = currentPos.positionID
            mtos = MaterialTolidOrderSerializer(instance=tolidInstance, data={"desc": dt}, partial=True)
            mtos.is_valid(raise_exception=True)
            mtos = mtos.save()

        pp = NotificationViewSet()

        pp.send_to_group_message_with_ws(987897866, 'کویل مصرف شد', 'group_material', {
            'body':
                'کویل در آدرس %s مصرف شد' % (
                    bs.desc['location']['locationTitle'] if bs.desc['location']['locationTitle'] else ''
                ),
            'alarm': 'al_succ'
        })

        return Response({
            'completed': itemsNotFinished == 0,
            'coil': MaterialTolidIOrdertemsSerializer(instance=msi).data
        })

    @list_route(methods=['post'])
    def getdates_of_showreport1(self, request, *args, **kwargs):
        limit = request.data.get('limit', 10)
        skip = request.data.get('skip', 0)
        limit = limit if limit is not None else 2
        skip = skip if skip is not None else 0

        datesOf = list(MaterialTolidOrder.objects.aggregate(
            {
                '$group':
                    {
                        '_id':
                            {
                                "$dateToString": {"format": "%Y-%m-%d", "date": "$forDate"}}
                        ,
                        'count':
                            {'$sum': 1},
                        'ids':
                            {'$addToSet': {'tolid_id': '$_id',
                                           'timeOf': {"$dateToString": {"format": "%H:%M:%S", "date": "$forDate"}}}},

                    }
            },
            {"$sort": {"_id": -1}},
            {"$skip": skip},
            {"$limit": limit}
        ))
        return Response({
            'result': datesOf,
            'limit': limit,
            'skip': skip
        })

    @list_route(methods=['post'])
    def getdates_of_showreport2(self, request, *args, **kwargs):
        limit = request.data.get('limit', 10)
        skip = request.data.get('skip', 0)
        limit = limit if limit is not None else 2
        skip = skip if skip is not None else 0

        datesOf = list(Barcodes.objects.aggregate(
            {
                '$group':
                    {
                        '_id':
                            {
                                "$dateToString": {"format": "%Y-%m-%d", "date": "$dateOfPost"}}
                        ,
                        'count':
                            {'$sum': 1},
                        'sumOfVorood': {
                            '$sum': '$desc.barcode.vazne_khales'
                        },
                        'ids':
                            {'$addToSet': {'barcode_id': '$_id',
                                           'timeOf': {"$dateToString": {"format": "%H:%M:%S", "date": "$dateOfPost"}}}},
                    }
            },
            {"$sort": {"_id": -1}},
            {"$skip": skip},
            {"$limit": limit}
        ))

        return Response({
            'result': datesOf,
            'limit': limit,
            'skip': skip
        })

    @list_route(methods=['post'])
    def showreport2(self, request, *args, **kwargs):
        dateOf = request.data['dateOf']['_id']

        datesOf = list(Barcodes.objects.filter(
            dateOfPost__gte=datetime.strptime(dateOf + " 00:00:00", "%Y-%m-%d %H:%M:%S"),
            dateOfPost__lte=datetime.strptime(dateOf + " 23:59:59", "%Y-%m-%d %H:%M:%S")).order_by('-dateOfPost'))
        datesOf = BarcodesSerializer(instance=datesOf, many=True).data
        sums = query(datesOf).sum(lambda x: x.get('desc', {}).get('barcode', {}).get('vazne_khales', 0))

        return Response({
            'sums': sums,
            'result': datesOf})

    @list_route(methods=['post'])
    def showreport1(self, request, *args, **kwargs):
        dateOf = request.data['dateOf']['_id']

        datesOf = list(MaterialTolidOrder.objects.filter(
            forDate__gte=datetime.strptime(dateOf + " 00:00:00", "%Y-%m-%d %H:%M:%S"),
            forDate__lte=datetime.strptime(dateOf + " 23:59:59", "%Y-%m-%d %H:%M:%S")).order_by('-forDate'))
        datesOf = MaterialTolidOrderSerializer(instance=datesOf, many=True).data
        sums = 0
        for dd in datesOf:
            dd['details'] = MaterialTolidOrderItems.objects.filter(linkMaterialTolid=dd['id'])
            dd['details'] = MaterialTolidIOrdertemsSerializer(instance=dd['details'], many=True).data
            dd['details'].append({'mizaneMasraf': query(dd['details']).sum(lambda x: x['mizaneMasraf'])})
            sums = sums + query(dd['details']).sum(lambda x: x['mizaneMasraf'])

        return Response({
            'sums': int(sums / 2),
            'result': datesOf})
