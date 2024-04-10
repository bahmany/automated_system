from datetime import datetime

from django.db.models import Q
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionDocumentSerializer
from amspApp.Material.models import MaterialConvSale
from amspApp.Material.serializers.WarehouseSerializer import MaterialConvSaleSerializer
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class MaterialConvSaleViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = MaterialConvSale.objects.all().order_by('-id')
    serializer_class = MaterialConvSaleSerializer

    pagination_class = DetailsPagination

    sheetdefs = [
        {'data': 'radeef', 'dataType': 'numeric', 'id': 1, 'numericFormat': {'pattern': '0,0'}, 'readOnly': False,
         'title': 'ردیف'},
        {'data': 'code_mavade_avalieh', 'dataType': 'numeric', 'id': 2, 'numericFormat': {'pattern': '0,0'},
         'readOnly': False, 'title': 'کد مواد اولیه'},
        {'data': 'keshavare_sazandeh', 'dataType': 'text', 'id': 3, 'numericFormat': {'pattern': '0,0'},
         'readOnly': False, 'title': 'کشور سازنده'},
        {'data': 'temper', 'dataType': 'numeric', 'id': 4, 'numericFormat': {'pattern': '0,0'}, 'readOnly': False,
         'title': 'تمپر'},
        {'data': 'sur', 'dataType': 'numeric', 'id': 5, 'numericFormat': {'pattern': '0,0'}, 'readOnly': False,
         'title': 'SUR'},
        {'data': 'zekhamat', 'dataType': 'numeric', 'id': 6, 'numericFormat': {'pattern': '0,0'}, 'readOnly': False,
         'title': 'ضخامت'},
        {'data': 'arz', 'dataType': 'numeric', 'id': 7, 'numericFormat': {'pattern': '0,0'}, 'readOnly': False,
         'title': 'عرض'},
        {'data': 'darajeh', 'dataType': 'numeric', 'id': 8, 'numericFormat': {'pattern': '0,0'}, 'readOnly': False,
         'title': 'درجه'},
        {'data': 'toole_boresh', 'dataType': 'numeric', 'id': 9, 'numericFormat': {'pattern': '0,0'}, 'readOnly': False,
         'title': 'طول برش'},
        {'data': 'mojoodi', 'dataType': 'numeric', 'id': 10, 'numericFormat': {'pattern': '0,0'}, 'readOnly': False,
         'title': 'موجودی'},
        {'data': 'pishforoosh_va_forookhteh', 'dataType': 'numeric', 'id': 11, 'numericFormat': {'pattern': '0,0'},
         'readOnly': False, 'title': 'پیش فروش و فروخته شده'},
        {'data': 'nahieh_2_va_keifi', 'dataType': 'numeric', 'id': 12, 'numericFormat': {'pattern': '0,0'},
         'readOnly': False, 'title': 'ناحیه ۲ و کیفی'},
        {'data': 'mozakereh', 'dataType': 'numeric', 'id': 13, 'numericFormat': {'pattern': '0,0'}, 'readOnly': False,
         'title': 'مذاکره'},
        {'data': 'mojoodi_ghabel_foroosh', 'dataType': 'numeric', 'id': 14, 'numericFormat': {'pattern': '0,0'},
         'readOnly': True, 'title': 'موجودی قابل فروش'},
        {'data': 'tozihat', 'dataType': 'text', 'id': 15, 'readOnly': False,
         'title': 'توضیحات'}]


    def checkPerm(self, req):
        if req.user.groups.filter(
                Q(name__contains="group_namayendgi_8_ostan")).count() > 0:
            raise Exception("مجوز دسترسی ندارید")

    def initialize_request(self, request, *args, **kwargs):
        self.checkPerm(request)
        return super(MaterialConvSaleViewSet, self).initialize_request(request, *args, **kwargs)


    @list_route(methods=["get"])
    def getColDefs(self, request, *args, **kwargs):
        return Response(self.sheetdefs)

    def getPositionDocByPosID(self, positionID):
        ps = PositionsDocument.objects.filter(positionID=positionID).order_by('-postDate').first()
        ps = PositionDocumentSerializer(instance=ps).data
        s = {"positionName": ps["profileName"], "positionchartName": ps["chartName"], "positionavatar": ps["avatar"]}
        return s

    def retrieve(self, request, *args, **kwargs):
        result = super(MaterialConvSaleViewSet, self).retrieve(request, *args, **kwargs)
        c = 2
        for d in result.data['desc']['details']:
            d['mojoodi_ghabel_foroosh'] = '=J%d-K%d-L%d-M%d' % (c, c, c, c,)
            c = c + 1
        return result

    def list(self, request, *args, **kwargs):
        result = super(MaterialConvSaleViewSet, self).list(request, *args, **kwargs)
        for r in result.data['results']:
            ins = self.getPositionDocByPosID(r['positionID'])
            ins2 = self.getPositionDocByPosID(r['desc']['lastEditPositionID'])
            r['creator'] = ins
            r['editor_creator'] = ins2

        return result

    @detail_route(methods=['get'])
    def CopyNew(self, request, *args, **kwargs):
        idOf = kwargs.get('id')
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        ser = self.queryset.get(id=kwargs.get('id'))
        ser = self.serializer_class(instance=ser).data
        del ser['id']
        ser = self.serializer_class(data=ser)
        ser.is_valid(raise_exception=True)
        ser = ser.save()
        ser = self.serializer_class(instance=ser).data
        return Response(ser)

    @detail_route(methods=['post'])
    def saveCovSale(self, request, *args, **kwargs):
        idOf = kwargs.get('id')
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        newValues = []
        for d in request.data:
            # values = d[s['id'] - 1]
            line = {}
            for s in self.sheetdefs:
                value = d[s['id'] - 1]
                keyname = s['data']
                line[keyname] = value
            newValues.append(line)

        if idOf == '0':
            dt = {
                'dateOfPost': datetime.now(),
                'positionID': posiIns.positionID,
                'desc': {
                    'details': newValues,
                    'edittimes': 0,
                    'lastEditDate': datetime.now(),
                    'lastEditPositionID': posiIns.positionID,
                }
            }
            ser = self.serializer_class(data=dt)
            ser.is_valid(raise_exception=True)
            ser = ser.save()
            ser = self.serializer_class(instance=ser).data
            return Response(ser)
        ser = self.queryset.get(id=kwargs.get('id'))
        dt = {
            'desc': {
                'details': newValues,
                'edittimes': ser.desc['edittimes'] + 1,
                'lastEditDate': datetime.now(),
                'lastEditPositionID': posiIns.positionID,
            }
        }
        ser = self.serializer_class(instance=ser, data=dt, partial=True)
        ser.is_valid(raise_exception=True)
        ser = ser.save()
        ser = self.serializer_class(instance=ser).data
        return Response(ser)
