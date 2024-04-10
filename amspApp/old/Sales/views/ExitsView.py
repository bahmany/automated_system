import uuid
from datetime import datetime, timedelta
from random import randint

from asq.initiators import query
from django.contrib.auth.models import Group
from django.shortcuts import render_to_response
from django.template import RequestContext
from mongoengine import Q
from django.db.models import Q as _q
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
import xml.etree.ElementTree as et
from amspApp.CompaniesManagment.Connections.models import ConnectionPools, Connections
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsViews import ConnectionsViewSet
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh, mil_to_sh_with_time, getCurrentYearShamsi, \
    sh_to_mil, getCurrentMonthShamsi, getMonthDays, get_filter_times, get_today_str, get_date_str
from amspApp.Infrustructures.Classes.convert_sqlresult_to_validstr import convert_sqlresultstr_to_valid_str, \
    convert_sqlresultstr_to_valid_numbers
from amspApp.Notifications.models import Notifications
from amspApp.Sales.models import Exits, lastExitID, ExtisFiles, ExitsSMS, ExitsSigns, SalesCustomerProfile, \
    HamkaranKhorooj, HamkaranKhoroojSigns, HamkaranKhoroojSMS, HamkaranKhoroojFiles, HamkaranCustomerNotes, \
    HamkaranKhoroojItems, HamkaranHavaleForoosh, HamkaranHavaleForooshOrderApprove, HamkaranIssuePermitItem

from amspApp.Sales.serializers.CustomerProfileSerializer import CustomerProfileSerializer, \
    HamkaranCustomerNotesSerializer
from amspApp.Sales.serializers.ExitsSerializer import ExitsSerializer, ExtisFilesSerializer, ExitsSMSSerializer, \
    ExitsSignSerializer
from amspApp.Sales.serializers.HavalehForooshSerializer import HavalehForooshSerializer, \
    HavalehForooshApproveSerializer, HamkaranIssuePermitItemSerializer
from amspApp.Sales.serializers.KhoroojSerializer import HamkaranKhoroojSerializer, KhoroojSMSSerializer, \
    HamkaranKhoroojFilesSerializer, HamkaranKhoroojSignsSerializer, HamkaranKhroojItemsSerializer
from amspApp.Sales.views.CustomerProfileView import CustomerProfileViewSet
from amspApp.Sales.views.SalesView import SalesViewSet

from amspApp._Share.ListPagination import DataTablesPagination, DetailsPagination
from amspApp._Share.colors import zenos_dichotomy, gen_colors
from amspApp.amspUser.views.UserView import UserViewSet
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset
from amspApp.tasks import sendSMS


class KhoroojViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = HamkaranKhorooj.objects.all().order_by('-exp__t0_CreationDate')
    serializer_class = HamkaranKhoroojSerializer
    pagination_class = DetailsPagination

    @staticmethod
    def get_sign_title(sign_index):
        if sign_index == 1:
            return " امضا صادره کننده - انباردار "
        if sign_index == 2:
            return " امضا تایید کننده - سرپرست حسابداری "
        if sign_index == 3:
            return "امضا تصویب کننده - مدیرعامل یا مدیرمالی "
        if sign_index == 4:
            return "امضای نماینده حراست مرحله اول"
        if sign_index == 5:
            return "امضای نماینده حراست تحویل به راننده"
        return "غیر معتبر"

    kgs = ['66', '69', '75', '77', '85', '86', '87', '88']

    @list_route(methods=['GET'])
    def get_today_exit_number(self, request, *args, **kwargs):
        alldates = get_filter_times()
        result = list(HamkaranKhoroojItems.objects.aggregate(
            {
                '$match': {
                    'item.Date': {"$lte": alldates['end_of_today'], "$gte": alldates['start_of_today']},
                    'item.Code': {"$regex": "^[" + '|'.join(self.kgs) + "]", '$options': 'i'}
                }
            }, {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$item.Quantity"}
                }
            }
        ))
        result = list(result)
        if len(result) == 0:
            today = get_today_str()
            today['result'] = 0
            return Response(today)

        today = get_today_str()
        today['result'] = int(result / 1000)
        return Response(today)

    @list_route(methods=['GET'])
    def get_today_exit_today_for_chart(self, request, *args, **kwargs):
        alldates = get_filter_times()
        result = list(HamkaranKhoroojItems.objects.aggregate(
            {
                '$match': {
                    'item.Date': {"$lte": alldates['end_of_today'], "$gte": alldates['start_of_today']},
                    'item.Code': {"$regex": "^[" + '|'.join(self.kgs) + "]", '$options': 'i'}
                }
            }, {
                "$group": {
                    "_id": '$item.CounterpartEntityText',
                    "total": {"$sum": "$item.Quantity"}
                }
            }, {
                "$sort": {"total": -1}
            }
        ))
        labels = [x['_id'] for x in result]
        data = [int(x['total'] / 1000) for x in result]

        result = {
            'datasets': [
                {
                    'backgroundColor': [gen_colors()[randint(0, 9)] for x in labels],
                    'label': 'خروج امروز - تناژ',
                    'data': data
                }
            ],
            'labels': labels
        }
        return Response(result)

    @list_route(methods=['GET'])
    def get_today_exit_today_for_chart_by_product(self, request, *args, **kwargs):
        alldates = get_filter_times()
        result = list(HamkaranKhoroojItems.objects.aggregate(
            {
                '$match': {
                    'item.Date': {"$lte": alldates['end_of_today'], "$gte": alldates['start_of_today']},
                    'item.Code': {"$regex": "^[" + '|'.join(self.kgs) + "]", '$options': 'i'}
                }
            }, {
                "$group": {
                    "_id": '$item.PartName',
                    "total": {"$sum": "$item.Quantity"}
                }
            }, {
                "$sort": {"total": -1}
            }
        ))
        labels = [x['_id'] for x in result]
        data = [int(x['total'] / 1000) for x in result]

        result = {
            'datasets': [
                {
                    'backgroundColor': [gen_colors()[randint(0, 9)] for x in labels],
                    'label': 'خروج امروز - تناژ',
                    'data': data
                }
            ],
            'labels': labels
        }
        return Response(result)

    @list_route(methods=['GET'])
    def get_today_exit_week_for_chart(self, request, *args, **kwargs):
        alldates = get_filter_times()
        result = list(HamkaranKhoroojItems.objects.aggregate(
            {
                '$match': {
                    'item.Date': {"$lte": alldates['current_week_end'], "$gte": alldates['current_week_start']},
                    'item.Code': {"$regex": "^[" + '|'.join(self.kgs) + "]", '$options': 'i'}
                }
            }, {
                "$group": {
                    "_id": '$item.CounterpartEntityText',
                    "total": {"$sum": "$item.Quantity"}
                }
            }, {
                "$sort": {"total": -1}
            }
        ))
        labels = [x['_id'] for x in result]
        data = [int(x['total'] / 1000) for x in result]

        result = {
            'datasets': [
                {
                    'backgroundColor': [gen_colors()[randint(0, 9)] for x in labels],
                    'label': 'خروج این هفته - تناژ',
                    'data': data
                }
            ],
            'labels': labels
        }
        return Response(result)

    @list_route(methods=['GET'])
    def get_today_exit_week_for_chart_by_product(self, request, *args, **kwargs):
        alldates = get_filter_times()
        result = list(HamkaranKhoroojItems.objects.aggregate(
            {
                '$match': {
                    'item.Date': {"$lte": alldates['current_week_end'], "$gte": alldates['current_week_start']},
                    'item.Code': {"$regex": "^[" + '|'.join(self.kgs) + "]", '$options': 'i'}
                }
            }, {
                "$group": {
                    "_id": '$item.PartName',
                    "total": {"$sum": "$item.Quantity"}
                }
            }, {
                "$sort": {"total": -1}
            }
        ))
        labels = [x['_id'] for x in result]
        data = [int(x['total'] / 1000) for x in result]

        result = {
            'datasets': [
                {
                    'backgroundColor': [gen_colors()[randint(0, 9)] for x in labels],
                    'label': 'خروج این هفته - تناژ',
                    'data': data
                }
            ],
            'labels': labels
        }
        return Response(result)

    @detail_route(methods=['GET'])
    def gotonext(self, request, *args, **kwargs):
        id = kwargs.get("id")
        fff = HamkaranKhorooj.objects.filter(id__gt=id).order_by("exp__t0_CreationDate").first()
        if not fff:
            return Response({"id": ""})
        return Response({'id': str(fff.id)})

    def checkPerm(self, req):
        qr = _q(name__contains="ext") | _q(name="group_namayendgi_8_ostan")
        if req.user.groups.filter(qr).count() == 0:
            raise Exception("مجوز دسترسی ندارید")

    def list(self, request, *args, **kwargs):
        self.checkPerm(request)

        searchStr = request.query_params.get("search")
        qq = Q()

        if searchStr:
            if searchStr != "":
                qq = Q(exp__t0_CounterpartEntityText__icontains=searchStr)
                qq |= Q(exp__t1_Name__icontains=searchStr)
                qq |= Q(exp__t1_StockCaption__icontains=searchStr)
                qq |= Q(exp__t1_DelivererOrReceiverCaption__icontains=searchStr)
                qq |= Q(exp__t2_String__icontains=searchStr)
                qq |= Q(exp__t2_String2__icontains=searchStr)
                qq |= Q(exp__t2_String3__icontains=searchStr)
                qq |= Q(exp__t2_String4__icontains=searchStr)
                qq |= Q(exp__t3_noe_vasileh__icontains=searchStr)
                qq |= Q(exp__t4_name_barbari__icontains=searchStr)
                qq |= Q(exp__t0_Number__icontains=searchStr)
                if searchStr.isdigit():
                    qq |= Q(exp__t2_Number3=int(searchStr))
                    qq |= Q(exp__t2_Number4=int(searchStr))
                    qq |= Q(exp__t2_Number5=int(searchStr))
                    qq |= Q(exp__t2_Number6=int(searchStr))

        if request.user.groups.filter(name="group_namayendgi_8_ostan").count() > 0:
            customers = SalesCustomerProfile.objects.filter(exp__namayandegi_8_ostaan=True)
            customers_codes = [customer.hamkaranCode + "    " if customer.hamkaranCode != None else "-1" for customer in
                               customers]
            # فیلتر تاریخش طوری باشد که بعد از اردیبهشت سال ۱۴۰۰ را بتواند ببیند
            dateof = datetime.strptime('2021-04-21', '%Y-%m-%d')
            self.queryset = self.queryset.filter(exp__DLRef__in=customers_codes, exp__VchDate__gte=dateof)

        self.queryset = self.queryset.filter(qq)
        result = super(KhoroojViewSet, self).list(request, *args, **kwargs)
        return result

    def get_start_and_end_date_from_calendar_week(self, year, calendar_week):
        monday = datetime.strptime(f'{year}-{calendar_week}-1', "%Y-%W-%w")
        return monday, monday + timedelta(days=6.9)

    @list_route(methods=['GET'])
    def get_report(self, request, *args, **kwargs):
        type_of_report = request.query_params.get('typeof')
        currenttime = datetime.now()
        last_hour_date_time = currenttime - timedelta(hours=12)

        if type_of_report == '1':
            last_hour_date_time = currenttime - timedelta(hours=1)
        if type_of_report == '2':
            last_hour_date_time = currenttime - timedelta(hours=3)
        if type_of_report == '3':
            last_hour_date_time = currenttime - timedelta(hours=5)
        if type_of_report == '4':
            last_hour_date_time = datetime.now().replace(hour=0, minute=0, second=1, microsecond=9)
        if type_of_report == '5':
            currenttime = (datetime.now() - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=9)
            last_hour_date_time = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=1,
                                                                               microsecond=9)
        if type_of_report == '6':
            current_week_number = datetime.now().strftime("%V")
            if datetime.now().strftime("%A") == 'Saturday':
                current_week_number = str(int(current_week_number) + 1)
            current_year = datetime.now().year
            _from, _to = self.get_start_and_end_date_from_calendar_week(current_year, current_week_number)
            _from = _from.replace(hour=0, minute=0, second=0, microsecond=1)
            _from = _from - timedelta(days=2)
            _to = _to.replace(hour=23, minute=59, second=59, microsecond=999)
            _to = _to - timedelta(days=2)
            currenttime = _to
            last_hour_date_time = _from

        if type_of_report == '7':
            current_week_number = str(int(datetime.now().strftime("%V")) - 1)
            if datetime.now().strftime("%A") == 'Saturday':
                current_week_number = str(int(current_week_number) + 1)
            current_year = datetime.now().year
            _from, _to = self.get_start_and_end_date_from_calendar_week(current_year, current_week_number)
            _from = _from.replace(hour=0, minute=0, second=0, microsecond=1)
            _from = _from - timedelta(days=2)
            _to = _to.replace(hour=23, minute=59, second=59, microsecond=999)
            _to = _to - timedelta(days=2)
            currenttime = _to
            last_hour_date_time = _from

        if type_of_report == '8':
            _from = datetime.strptime(
                sh_to_mil("{}/{}/{}".format(getCurrentYearShamsi(), getCurrentMonthShamsi(), "01")) + " 00:00:00",
                "%Y/%m/%d %H:%M:%S")
            _to = datetime.strptime(
                sh_to_mil("{}/{}/{}".format(
                    getCurrentYearShamsi(),
                    getCurrentMonthShamsi(),
                    str(getMonthDays(getCurrentMonthShamsi()))
                )) + " 23:59:59",
                "%Y/%m/%d %H:%M:%S")
            currenttime = _to - timedelta(days=1)
            last_hour_date_time = _from

        if type_of_report == '9':
            cc = int(getCurrentMonthShamsi()) - 1
            from_month = str(cc) if cc != 1 else "12"
            from_year = getCurrentYearShamsi() if cc != 1 else str(int(getCurrentYearShamsi()) - 1)

            _from = datetime.strptime(
                sh_to_mil("{}/{}/{}".format(from_year, from_month, "01")) + " 00:00:00",
                "%Y/%m/%d %H:%M:%S")

            _to = datetime.strptime(
                sh_to_mil(
                    "{}/{}/{}".format(from_year, from_month, str(getMonthDays(getCurrentMonthShamsi())))) + " 23:59:59",
                "%Y/%m/%d %H:%M:%S")
            currenttime = _to
            last_hour_date_time = _from

        if type_of_report == '10':
            startdate = getCurrentYearShamsi()
            enddate = getCurrentYearShamsi()
            currenttime = datetime.strptime(sh_to_mil(enddate + "/12/29") + " 23:59:59", "%Y/%m/%d %H:%M:%S")
            last_hour_date_time = datetime.strptime(sh_to_mil(startdate + '/1/1') + ' 00:00:01', "%Y/%m/%d %H:%M:%S")

        if type_of_report == '11':
            startdate = str(int(getCurrentYearShamsi()) - 1)
            enddate = str(int(getCurrentYearShamsi()) - 1)
            currenttime = datetime.strptime(sh_to_mil(enddate + "/12/29") + " 23:59:59", "%Y/%m/%d %H:%M:%S")
            last_hour_date_time = datetime.strptime(sh_to_mil(startdate + '/1/1') + ' 00:00:01', "%Y/%m/%d %H:%M:%S")

        result = list(HamkaranKhorooj.objects.aggregate(
            {
                '$match': {
                    '$and': [
                        {'exp.t0_CreationDate': {"$lte": currenttime}},
                        {'exp.t0_CreationDate': {"$gte": last_hour_date_time}},
                    ]
                }
            },
            {
                '$lookup':
                    {
                        'from': 'hamkaran_khorooj_items',
                        'localField': 'ID',
                        'foreignField': 'item.InventoryVoucherRef',
                        'as': 'items'
                    }
            },
            {
                '$unwind':
                    {
                        'path': '$items',
                        'preserveNullAndEmptyArrays': True
                    }
            },
            {
                '$group': {
                    '_id': {
                        't0_CounterpartDLCode': '$exp.t0_CounterpartDLCode',
                        'PartUnit': '$items.item.PartUnit'
                    },
                    'name': {'$first': '$exp.t0_CounterpartEntityText'},
                    't0_CounterpartEntityRef': {'$first': '$exp.t0_CounterpartEntityRef'},
                    'sumof_qty': {'$sum': '$items.item.Quantity'},
                }
            }
            ,
            {
                '$unwind':
                    {
                        'path': '$_id',
                        'preserveNullAndEmptyArrays': True
                    }
            },
            {
                '$sort':
                    {
                        'sumof_qty': -1
                    }
            }

        ))
        dt = {}
        dt['result'] = result
        dt['startdate'] = last_hour_date_time
        dt['enddate'] = currenttime
        dt['total_kg'] = query(result).where(lambda x: x['_id']['PartUnit'] == 'کیلوگرم').sum(lambda x: x['sumof_qty'])
        dt['total_cnt'] = query(result).where(lambda x: x['_id']['PartUnit'] == 'عدد').sum(lambda x: x['sumof_qty'])

        return Response(dt)

    @list_route(methods=['GET'])
    def get_trace_report(self, request, *args, **kwargs):
        havaleh_foroosh_instances = HamkaranHavaleForoosh.objects.all().limit(100).order_by('-ID')
        havaleh_foroosh_instances = HavalehForooshSerializer(instance=havaleh_foroosh_instances, many=True).data

        for h in havaleh_foroosh_instances:
            hhfoa = HamkaranHavaleForooshOrderApprove.objects.filter(havalehForooshLink=h['id'])
            hhfoa = HavalehForooshApproveSerializer(instance=hhfoa, many=True).data
            h['approves'] = hhfoa
            for hh in h['approves']:
                for ccc in hh['item']['items']:
                    ccc['exits'] = []
                    inss = HamkaranIssuePermitItem.objects.filter(exp__ProductSourceItemRef=ccc['OrderItemID'])
                    inss = HamkaranIssuePermitItemSerializer(instance=inss, many=True).data
                    for iii in inss:
                        exxx = HamkaranKhoroojItems.objects.filter(item__ReferenceRef=iii['exp']['IssuePermitItemID'])
                        exxx = HamkaranKhroojItemsSerializer(instance=exxx, many=True).data
                        ccc['exits'].extend(exxx)
                    ccc['exits_totals'] = {
                        'sumof': 0
                    }
                    if len(ccc['exits']) > 0:
                        ccc['exits_totals']['sumof'] = query(ccc['exits']).sum(lambda x: x['item']['MajorUnitQuantity'])

        return Response(havaleh_foroosh_instances)
        # objs = HamkaranHavaleForoosh.objects.aggregate(
        #     {
        #         '$lookup': {
        #             'from': 'hamkaran_issue_permit',
        #             'localField': 'ID',
        #             'foreignField': 'exp.ReferenceRef',
        #             'as': 'issue'
        #         }}, {
        #         '$unwind': {
        #             'path': '$issue',
        #             'preserveNullAndEmptyArrays': True
        #
        #         }}, {
        #         '$lookup': {
        #             'from': 'hamkaran_issue_permit_item',
        #             'localField': 'issue.exp.IssuePermitID',
        #             'foreignField': 'exp.IssuePermitRef',
        #             'as': 'issue.issue_items'
        #         }}, {
        #         '$sort': {'tarikheSodoor': -1}
        #     },
        #     {"$skip": 0},
        #     {"$limit": 50}
        # )
        #
        # objs = list(objs)
        #
        # for obj in objs:
        #     if len(obj['issue'].keys()) != 0:
        #         if len(obj['issue']['issue_items']) != 0:
        #             for issue in obj['issue']['issue_items']:
        #                 order_item_id = int(et.fromstring(issue['exp']['ExtraData']).attrib['ProductSourceItemRef'])
        #
        #                 orders_items = HamkaranHavaleForooshOrderApprove.objects.aggregate(
        #                     {'$unwind': {
        #                         'path': '$item.items',
        #                         'preserveNullAndEmptyArrays': True
        #                     }},
        #                     {'$project': {
        #                         'item': '$item.items'
        #                     }},
        #                     {
        #                         '$match': {
        #                             'item.OrderItemID': order_item_id
        #                         }}
        #                 )
        #
        #                 orders_item = list(orders_items)
        #                 issue['orders_item'] = orders_item
        #                 exit_item_id = issue['exp']['IssuePermitItemID']
        #                 exit_instance = HamkaranKhoroojItems.objects.filter(item__ReferenceRef=exit_item_id).first()
        #                 if exit_instance:
        #                     issue['exit_item'] = dict(HamkaranKhroojItemsSerializer(instance=exit_instance).data)

        # return Response({})

    @detail_route(methods=['GET'])
    def gotoprev(self, request, *args, **kwargs):
        id = kwargs.get("id")
        fff = HamkaranKhorooj.objects.filter(id__lt=id).order_by("-exp__t0_CreationDate").first()
        if not fff:
            return Response({"id": ""})
        return Response({'id': str(fff.id)})

    @detail_route(methods=["POST"])
    def saveFiles(self, request, *args, **kwargs):
        # VchHdrId = int(request.data["VchHdrId"])
        HamkaranKhoroojFiles.objects.filter(khoroojLink=request.data["id"]).delete()
        ser = HamkaranKhoroojFilesSerializer(
            data={
                "Files": request.data["Files"],
                "khoroojLink": request.data["id"]
            }
        )
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    def retrieve(self, request, *args, **kwargs):
        result = super(KhoroojViewSet, self).retrieve(request, *args, **kwargs)
        # حذف از نوتیفیکیشن
        q1 = Q(type=4)
        q2 = Q(userID=request.user.id)
        q3 = Q(extra__exitID=result.data['id'])
        qq = q1 & q2 & q3
        Notifications.objects.filter(qq).delete()
        _mutable = request.data._mutable
        request.query_params._mutable = True
        request.query_params['typeof'] = 6
        request.query_params._mutable = False
        rr = KhoroojViewSet().get_report(request, *args, **kwargs)
        ss = query(rr.data['result']).where(
            lambda x: x['t0_CounterpartEntityRef'] == result.data['exp']['t0_CounterpartEntityRef']).to_list()
        kg = query(ss).where(lambda x: x['_id']['PartUnit'] == 'کیلوگرم').sum(lambda x: x['sumof_qty'])
        adad = query(ss).where(lambda x: x['_id']['PartUnit'] == 'عدد').sum(lambda x: x['sumof_qty'])
        ss = {}
        ss['kg'] = kg
        ss['adad'] = adad
        for i in result.data['items']:
            i['havaleh_foroosh_tarikh_sh'] = get_date_str(i.get('havaleh_foroosh_tarikh','')) if i.get('havaleh_foroosh_tarikh','')!= '' else ''
        result.data['report'] = ss
        # اینجا امضاها رو ذکر میکنیم
        # برای اینکه بتوانم راحت تر در موبایل نمایش دهم
        si1 = dict(title='انبار', name='', shamsi='', )
        si2 = dict(title='حسابداری', name='', shamsi='', )
        si3 = dict(title='مدیرعامل', name='', shamsi='', )
        si4 = dict(title='حراست', name='', shamsi='', )
        si5 = dict(title='حراست - خروج', name='', shamsi='', )

        def sigerr(step):
            sss = query(result.data['signs']).where(lambda x: x['whichStep'] == step).to_list()
            if len(sss) > 0:
                sss = sss[0]
                return sss
            return None

        if sigerr(1):
            si1['name'] = sigerr(1)['positionName']
            si1['shamsi'] = mil_to_sh_with_time(sigerr(1)['dateOfPost'])
            si1['comment'] = sigerr(1)['comment']

        if sigerr(2):
            si2['name'] = sigerr(2)['positionName']
            si2['shamsi'] = mil_to_sh_with_time(sigerr(2)['dateOfPost'])
            si2['comment'] = sigerr(2)['comment']
        if sigerr(3):
            si3['name'] = sigerr(3)['positionName']
            si3['shamsi'] = mil_to_sh_with_time(sigerr(3)['dateOfPost'])
            si3['comment'] = sigerr(3)['comment']
        if sigerr(4):
            si4['name'] = sigerr(4)['positionName']
            si4['shamsi'] = mil_to_sh_with_time(sigerr(4)['dateOfPost'])
            si4['comment'] = sigerr(4)['comment']
        if sigerr(5):
            si5['name'] = sigerr(5)['positionName']
            si5['shamsi'] = mil_to_sh_with_time(sigerr(5)['dateOfPost'])
            si5['comment'] = sigerr(5)['comment']

        result.data['signs_for'] = {}
        result.data['signs_for']['s1'] = si1
        result.data['signs_for']['s2'] = si2
        result.data['signs_for']['s3'] = si3
        result.data['signs_for']['s4'] = si4
        result.data['signs_for']['s5'] = si5

        # -----------------------
        return result

    @list_route(methods=["POST"])
    def sendSms(self, request, *args, **kwargs):
        khoroojInstance = HamkaranKhorooj.objects.get(id=request.data['id'])
        cells = HamkaranCustomerNotes.objects.filter(EntityRef=khoroojInstance.exp.get('t0_CounterpartDLCode'))
        if cells.count() == 0:
            return Response({'error': 'هیچ شماره موبایلی برای این خریدار ثبت نشده است'})

        cells = HamkaranCustomerNotesSerializer().get_phones(khoroojInstance.exp.get('t0_CounterpartEntityRef'))
        total_qty = int(HamkaranKhoroojItems.objects.filter(khoroojLink=khoroojInstance.id).sum('item.Quantity'))
        for c in cells:
            h = c.replace(" ", "")
            # generating link
            # -----------------------
            # -----------------------
            shortUID = uuid.uuid4().hex[:6].upper()
            sms_message = """با سلام
            میزان %s ک/عدد تحویل راننده %s بشماره پلاک %s باموبایل %s شد
            مشاهده حواله :
            https://app.****.com/xt/%s
            **** ****""" % (
                total_qty,
                khoroojInstance.exp['t2_String2'],
                khoroojInstance.exp['t2_String1'],
                khoroojInstance.exp['t2_String3'],
                shortUID,)
            cou = ExitsSMS.objects.filter(linkID=shortUID).count()
            if cou > 0:
                while True:
                    shortUID = uuid.uuid4().hex[:6].upper()
                    cou = ExitsSMS.objects.filter(linkID=shortUID).count()
                    if cou == 0:
                        break
            # -----------------------
            # -----------------------

            positionInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            sendSMS.delay(h, sms_message)
            # sendSMS(h, sms_message)
            dt = dict(
                khoroojLink=khoroojInstance.id,
                positionID=positionInstance.positionID,
                cellNoToSMS=h,
                # genID=cc.strResultMessage,
                # result=cc.SendSMS_SingleResult,
                dateOfPost=datetime.now(),
                genID="sent",
                result=False,
                msg=sms_message,
                linkID=shortUID
            )
            ser = KhoroojSMSSerializer(data=dt)
            ser.is_valid(raise_exception=True)
            ser.save()

        return Response({})

    @detail_route(methods=["GET"])
    def getSMS(self, request, *args, **kwargs):
        smss = HamkaranKhorooj.objects.get(id=kwargs['id'])
        exs = HamkaranKhoroojSigns.objects.filter(khoroojLink=smss.id).order_by("-id").first()
        smss = HamkaranKhoroojSMS.objects.filter(khoroojLink=smss.id)
        smss = KhoroojSMSSerializer(instance=smss, many=True).data
        for s in smss:
            if s.get("positionID"):
                positionInstance = PositionsDocument.objects.filter(positionID=s.get("positionID")).first()
                s["sendername"] = positionInstance.profileName
                s["senderchart"] = positionInstance.chartName

        return Response(smss)

    @detail_route(methods=["GET"])
    def getFiles(self, request, *args, **kwargs):
        if kwargs.get("id") == None:
            return Response({})
        if kwargs.get("id") == "undefined":
            return Response({})

        smss = HamkaranKhorooj.objects.get(id=kwargs['id'])
        lst = HamkaranKhoroojFiles.objects.filter(khoroojLink=smss.id)
        ser = HamkaranKhoroojFilesSerializer(instance=lst, many=True).data
        if len(ser) > 0:
            ser = ser[0]
        return Response(ser)

    @detail_route(methods=["GET"])
    def getDetailBarnamehSigns(self, request, *args, **kwargs):
        # getting signs
        exit = HamkaranKhorooj.objects.get(id=kwargs['id'])
        signs = list(HamkaranKhoroojSigns.objects.filter(khoroojLink=exit))
        codes = query(signs).distinct(lambda x: x.whichStep).select(lambda x: x.whichStep).to_list()
        ss = []
        for c in codes:
            current = query(signs).where(lambda x: x.whichStep == c).order_by_descending(
                lambda x: x.dateOfPost).to_list()
            if len(current) > 0:
                ss.append(current[0])
        # qrexit_ + exit_id + _ + positionID + _ +stepID
        if len(ss) > 0:
            signs = HamkaranKhoroojSignsSerializer(instance=ss, many=True).data
            for s in signs:
                ps = PositionsDocument.objects.filter(positionID=s["positionID"]).order_by('-postDate')
                ps = ps[0]
                s["positionName"] = ps["profileName"]
                s["positionchartName"] = ps["chartName"]
                s["positionavatar"] = ps["avatar"]
                s["signCount"] = len(signs)
                s["dateOfPost"] = mil_to_sh_with_time(s["dateOfPost"])
                s["hash"] = "https://app.****.com/SpecialApps/#!/home/Sales/kh/" + str(exit.id) + "/details"
                # s["hash"] = "http://app.****.ir/digital_sign/qrexit_" + str(exit.id) + "_" + str(ps.positionID) +
                #  "_" + str(s["whichStep"])
                del s["khoroojLink"]
        return Response(signs)

    @list_route(methods=["post"])
    def signExitFromMobile(self, request, *args, **kwargs):
        v = 1
        exitID = request.data['selid']
        signpass = request.data['entetedPass']
        exitInstance = HamkaranKhorooj.objects.get(id=exitID)
        exitSignsInstances = HamkaranKhoroojSigns.objects.filter(khoroojLink=exitID)
        exitSignsSerial = HamkaranKhoroojSignsSerializer(instance=exitSignsInstances, many=True).data
        signType = 1
        httppost = '/api/v1/hamkaranKhorooj/signExit/'
        withSMS = False
        stepID = 1
        st1 = query(exitSignsSerial).where(lambda x:x['whichStep']== 1).to_list()
        if len(st1) > 0:
            stepID = 1
        st2 = query(exitSignsSerial).where(lambda x:x['whichStep']== 2).to_list()
        if len(st2) > 0:
            stepID = 2
        st3 = query(exitSignsSerial).where(lambda x:x['whichStep']== 3).to_list()
        if len(st3) > 0:
            stepID = 3
        st4 = query(exitSignsSerial).where(lambda x:x['whichStep']== 4).to_list()
        if len(st4) > 0:
            stepID = 4
        st5 = query(exitSignsSerial).where(lambda x:x['whichStep']== 5).to_list()
        if len(st5) > 0:
            stepID = 5
            withSMS = True

        ss = {'exitID': exitID,
              'stepID': stepID+1,
              'signType': signType,
              'httppost': '/api/v1/hamkaranKhorooj/signExit/',
              'id': exitID,
              'withSMS': withSMS,
              'comment': request.data.get('comment'),
              'signpass': signpass}
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data.update(ss)
        request.data._mutable = False

        result = self.signExit(request, *args, **kwargs)
        return result

    @list_route(methods=["post"])
    def signExit(self, request, *args, **kwargs):
        if int(request.data.get("signType")) != 1:  # means exit sign
            return Response({'errorcode': 1, 'msg': 'این امضا برای این تابع مجاز نیست'})

        signPass = request.data.get('signpass')
        uvs = UserViewSet()
        signPassIsOK = uvs.checkUserSignPass(request.user, signPass)

        if not signPassIsOK:
            return Response({'errcode': 2, 'msg': 'رمز دوم اشتباه است'})

        exitID = request.data.get("exitID")
        stepNum = str(request.data.get("stepID"))
        if stepNum == "-1":  # means than finding latest step
            exitInstance = HamkaranKhorooj.objects.get(id=exitID)
            exitSignsInstance = HamkaranKhoroojSigns.objects.filter(exitsLink=exitInstance).order_by(
                "-whichStep").first()
            stepNum = str(exitSignsInstance.whichStep + 1)

        positionInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        exitInstance = HamkaranKhorooj.objects.get(id=exitID)
        groupName = "group_extis_permited_to_view_" + stepNum
        group = Group.objects.filter(name=groupName)
        if group.count() == 0:
            return Response({
                "errcode": 1,
                "msg": "ردیف امضاها تکمیل شده است"
            })
            # raise Exception("1_" + groupName + " does not created Mohammad Please create it !")
        # user = MyUser.objects.get(id = positionInstance.userID)
        group = group[0]
        isAllowed = group.user_set.all().filter(id=positionInstance.userID).count()
        if isAllowed == 0:
            return Response({
                "errcode": 2,
                "msg": "شما مجور امضا زدن ندارید"
            })
            # raise Exception("2_" + str(positionInstance.userID) + " does not have permission !")
        dt = {
            "positionID": positionInstance.positionID,
            "khoroojLink": exitInstance.id,
            "whichStep": int(stepNum),
            "dateOfPost": datetime.now(),
            "comment": request.data.get("comment"),
        }

        # ------------------------------------------------------------
        # ------------------------------------------------------------
        # ------------------------------------------------------------
        # checking if previous sign signed
        # checking hierarchy of signs
        currentStep = int(stepNum)
        for c in range(1, currentStep):
            countOfPrevStep = HamkaranKhoroojSigns.objects.filter(
                khoroojLink=exitInstance.id,
                whichStep=c
            ).count()
            if countOfPrevStep == 0:
                return Response({
                    "errcode": 3,
                    "msg": "ترتیب امضا رعایت نشده است لطفا از امضای امضا کننده های قبلی اطمینان پیدا کنید"
                })
                # raise Exception("3_" +
                # str(positionInstance.userID) + " signed before previous signs > person before you must sgn first !")
        # --------------------------------------------------------------
        # --------------------------------------------------------------
        # --------------------------------------------------------------
        ppp = dt
        del ppp['dateOfPost']
        countOfSigns = HamkaranKhoroojSigns.objects.filter(**ppp).count()
        if countOfSigns > 0:
            return Response({
                "errcode": 4,
                "msg": "شما قبلا امضا زده اید - لطفا صبر کنید و صفحه را رفرش کنید"
            })
            # raise Exception("4_" + str(positionInstance.userID) + " you have signed it before why ??")

        # -----------------------------------------------
        # now removing current notifications of user
        Notifications.objects.filter(
            extra__exitID=exitID
        ).delete()

        # -----------------------------------------------
        # -----------------------------------------------
        # -----------------------------------------------
        dt['dateOfPost'] = datetime.now()
        ser = HamkaranKhoroojSignsSerializer(data=dt)
        ser.is_valid(raise_exception=True)
        ser.save()

        if currentStep == 5:
            self.sendSms(request, *args, **kwargs)
        #         if currentStep == 5:
        #             # getting customer profile to sms
        #             customerProfile = SalesCustomerProfile.objects.filter(
        #                 hamkaranCode=exitInstance.item["DLRef"].replace(' ', '')
        #             )
        #             if customerProfile.count() > 0:
        #                 pass
        #         #                 sendSMS.delay(
        #         #                     SalesCustomerProfile.objects.filter(
        #         #                         hamkaranCode=exitInstance.item["DLRef"].replace(' ', '')
        #         #                     )[0].exp["contact"]["cell"],
        #         #                     """با سلام
        #         # میزان 0کیلو تحویل راننده جلال عالی پور هفشجانی بشماره پلاک 973ع54-43 باموبایل 0913-183-3139 شد
        #         # مشاهده حواله :
        #         # http://app.****.ir/xt/::suid
        #         # **** ****
        #         #                     """.replace("", "")
        #         #
        #         #                 )
        #         if request.data.get('withSMS'):
        #             cellno = request.data.get('cellno')
        #             smms = """با سلام
        # امضای شما در حواله ی خروج با کد %s ثبت شده است
        # تاریخ امضا %s
        # میزان خروجی %s
        # نام مشتری %s
        # **** ****""" % (
        #                 request.data.get('exitID'),
        #                 mil_to_sh_with_time(datetime.now()),
        #                 exitInstance.item.get('TotalQty'),
        #                 exitInstance.item.get('DLTitle'),
        #             )
        #             sendSMS.delay(cellno, smms)
        return Response(ser.data)


"""

این کلاس پایینی برای خروج های قدیمی هستند

"""


class ExitsViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Exits.objects.all().order_by("-item__VchHdrId")
    serializer_class = ExitsSerializer
    pagination_class = DataTablesPagination

    """
    permitted group for coming to exitis :
    group_extis_permited_to_view

    qrcode signature format :
    type = qrexit_
    qrexit_ + exit_id + _ + positionID

    steps:
     group_extis_permited_to_view_1
     group_extis_permited_to_view_2
     group_extis_permited_to_view_3
     group_extis_permited_to_view_4
     group_extis_permited_to_view_5

    """

    @staticmethod
    def get_sign_title(sign_index):
        if sign_index == 1:
            return " امضا صادره کننده - انباردار "
        if sign_index == 2:
            return " امضا تایید کننده - سرپرست حسابداری "
        if sign_index == 3:
            return "امضا تصویب کننده - مدیرعامل یا مدیرمالی "
        if sign_index == 4:
            return "امضای نماینده حراست مرحله اول"
        if sign_index == 5:
            return "امضای نماینده حراست تحویل به راننده"
        return "غیر معتبر"

    def mapHamkaran(self):
        # return
        lastVchHdrId = lastExitID.objects.first()
        if lastVchHdrId == None:
            ll = lastExitID(lastVchHdrId=0)
            ll.save()
            lastVchHdrId = ll

        pool = ConnectionPools.objects.get(name="AccCustomeTrans")
        sql = pool.sqls[0]["code"]
        sql = sql.replace("str__lessthan", " >= " + str(lastVchHdrId.lastVchHdrId + 1))
        sql = sql.replace("<:", "")
        sql = sql.replace(":>", "")
        connection = Connections.objects.get(databaseName="sgdb")
        connection = ConnectionsViewSet().getConnection(connection)
        connection.execute(sql)
        sql_res = connection.fetchall()

        sql_res = convert_sqlresultstr_to_valid_str(sql_res)
        sql_res = convert_sqlresultstr_to_valid_numbers(sql_res)

        for s in reversed(sql_res):
            dt = {'item': s}
            countOf = Exits.objects.filter(item__VchHdrId=s.get("VchHdrId")).count()
            if countOf == 0:
                cnOf = lastExitID.objects.filter(lastVchHdrId=s.get("VchHdrId")).count()
                if cnOf == 0:
                    ss = ExitsSerializer(data=dt)
                    ss.is_valid(raise_exception=True)
                    ss.save()
                    lastExitID.objects.all().delete()
                    lastExitID(lastVchHdrId=s.get("VchHdrId")).save()

    @list_route(methods=["GET"])
    def updateLatest50ChangesFromHamkaran(self, request, *args, **kwargs):
        pool = ConnectionPools.objects.get(name="AccAcutomeTransUpdateTop50")
        sql = pool.sqls[0]["code"]
        connection = Connections.objects.get(databaseName="sgdb")
        connection = ConnectionsViewSet().getConnection(connection)
        connection.execute(sql)
        sql_res = connection.fetchall()

        sql_res = convert_sqlresultstr_to_valid_str(sql_res)
        sql_res = convert_sqlresultstr_to_valid_numbers(sql_res)

        for s in sql_res:
            exit = Exits.objects.filter(item__VchHdrId=s["VchHdrId"])
            if exit.count() > 0:
                exit = exit[0]
                ffff = exit.item

                # ittt = exit.item.update()
                ffff.update(s)
                exit.update(set__item=ffff)
        return Response({})

    @list_route(methods=["post"])
    def signExit(self, request, *args, **kwargs):
        if int(request.data.get("signType")) != 1:  # means exit sign
            return Response({'errorcode': 1, 'msg': 'این امضا برای این تابع مجاز نیست'})

        signPass = request.data.get('signpass')
        uvs = UserViewSet()
        signPassIsOK = uvs.checkUserSignPass(request.user, signPass)

        if not signPassIsOK:
            return Response({'errcode': 2, 'msg': 'رمز دوم اشتباه است'})

        exitID = request.data.get("exitID")
        stepNum = str(request.data.get("stepID"))
        if stepNum == "-1":  # means than finding latest step
            exitInstance = Exits.objects.get(id=request.data.get("exitID"))
            exitSignsInstance = ExitsSigns.objects.filter(exitsLink=exitInstance).order_by("-whichStep").first()
            stepNum = str(exitSignsInstance.whichStep + 1)

        positionInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        exitInstance = Exits.objects.get(id=exitID)
        groupName = "group_extis_permited_to_view_" + stepNum
        group = Group.objects.filter(name=groupName)
        if group.count() == 0:
            return Response(
                {
                    "errcode": 1,
                    "msg": "گروه های عملیاتی توسط بهمنی ساخته نشده اند"
                }
            )
            # raise Exception("1_" + groupName + " does not created Mohammad Please create it !")
        # user = MyUser.objects.get(id = positionInstance.userID)
        group = group[0]
        isAllowed = group.user_set.all().filter(id=positionInstance.userID).count()
        if isAllowed == 0:
            return Response({
                "errcode": 2,
                "msg": "شما مجور امضا زدن ندارید"
            })
            # raise Exception("2_" + str(positionInstance.userID) + " does not have permission !")
        dt = {
            "positionID": positionInstance.positionID,
            "exitsLink": exitID,
            "whichStep": int(stepNum),
            "dateOfPost": datetime.now(),
            "comment": request.data.get("comment"),
        }

        # ------------------------------------------------------------
        # ------------------------------------------------------------
        # ------------------------------------------------------------
        # checking if previous sign signed
        # checking hierarchy of signs
        currentStep = int(stepNum)
        for c in range(1, currentStep):
            countOfPrevStep = ExitsSigns.objects.filter(
                exitsLink=exitID,
                whichStep=c
            ).count()
            if countOfPrevStep == 0:
                return Response({
                    "errcode": 3,
                    "msg": "ترتیب امضا رعایت نشده است لطفا از امضای امضا کننده های قبلی اطمینان پیدا کنید"
                })
                # raise Exception("3_" +
                # str(positionInstance.userID) + " signed before previous signs > person before you must sgn first !")
        # --------------------------------------------------------------
        # --------------------------------------------------------------
        # --------------------------------------------------------------

        countOfSigns = ExitsSigns.objects.filter(**dt).count()
        if countOfSigns > 0:
            return Response({
                "errcode": 4,
                "msg": "شما قبلا امضا زده اید - لطفا صبر کنید و صفحه را رفرش کنید"
            })
            # raise Exception("4_" + str(positionInstance.userID) + " you have signed it before why ??")

        # -----------------------------------------------
        # now removing current notifications of user
        Notifications.objects.filter(
            extra__exitID=exitID
        ).delete()

        # -----------------------------------------------
        # -----------------------------------------------
        # -----------------------------------------------

        ser = ExitsSignSerializer(data=dt)
        ser.is_valid(raise_exception=True)
        ser.save()
        if currentStep == 5:
            # getting customer profile to sms
            customerProfile = SalesCustomerProfile.objects.filter(
                hamkaranCode=exitInstance.item["DLRef"].replace(' ', '')
            )
            if customerProfile.count() > 0:
                pass
        #                 sendSMS.delay(
        #                     SalesCustomerProfile.objects.filter(
        #                         hamkaranCode=exitInstance.item["DLRef"].replace(' ', '')
        #                     )[0].exp["contact"]["cell"],
        #                     """با سلام
        # میزان 0کیلو تحویل راننده جلال عالی پور هفشجانی بشماره پلاک 973ع54-43 باموبایل 0913-183-3139 شد
        # مشاهده حواله :
        # http://app.****.ir/xt/::suid
        # **** ****
        #                     """.replace("", "")
        #
        #                 )
        if request.data.get('withSMS'):
            cellno = request.data.get('cellno')
            smms = """با سلام
امضای شما در حواله ی خروج با کد %s ثبت شده است
تاریخ امضا %s
میزان خروجی %s
نام مشتری %s
**** ****""" % (
                request.data.get('exitID'),
                mil_to_sh_with_time(datetime.now()),
                exitInstance.item.get('TotalQty'),
                exitInstance.item.get('DLTitle'),
            )
            sendSMS.delay(cellno, smms)
        return Response(ser.data)

    def retrieve(self, request, *args, **kwargs):
        result = super(ExitsViewSet, self).retrieve(request, *args, **kwargs)
        customer = CustomerProfileViewSet().convertDLtoCustomer(result.data["item"].get("DLRef").replace(" ", ""))
        # means دفتر مرکزی تهران
        if len(customer) == 0:
            profile = []
            profile.append({
                'id': '0',
                'desc': None,
                'hamkaranCode': '0',
                'name': 'هدیه یا دفتر تهران',
            })
        else:
            profile = SalesCustomerProfile.objects.filter(hamkaranCode=str(customer[0]['CstmrCode']))
            profile = CustomerProfileSerializer(instance=profile, many=True).data

        if len(profile) > 0:
            profile = profile[0]
        else:
            profile = {
                "name": result.data["item"]["CntrprtTitle"]
            }

        result.data["profile"] = profile
        return result

    def checkPerm(self, req):
        qr = _q(name__contains="ext") | _q(name="group_namayendgi_8_ostan")
        if req.user.groups.filter(qr).count() == 0:
            raise Exception("مجوز دسترسی ندارید")

    def list(self, request, *args, **kwargs):
        self.checkPerm(request)
        self.mapHamkaran()
        self.pagination_class = DetailsPagination
        # self.pagination_class.per_page = 30
        # self.pagination_class.max_page_size = 30
        self.updateLatest50ChangesFromHamkaran(request, args, kwargs)
        searchStr = request.query_params.get("search")
        qq = Q()

        if searchStr:
            if searchStr != "":
                qq = Q(item__Driver__icontains=searchStr)
                qq |= Q(item__RealTransNo__icontains=searchStr)
                qq |= Q(item__NationalCode__icontains=searchStr)
                qq |= Q(item__ZipCode__icontains=searchStr)
                qq |= Q(item__Phone__icontains=searchStr)
                qq |= Q(item__LicencNo__icontains=searchStr)
                qq |= Q(item__CntrprtTitle__icontains=searchStr)
                qq |= Q(item__CreatorName__icontains=searchStr)
                qq |= Q(item__TransCmpName__icontains=searchStr)
                qq |= Q(item__CarNumber__icontains=searchStr)
                qq |= Q(item__StockName__icontains=searchStr)
                if searchStr.isdigit():
                    qq |= Q(item__GrossWeigth=int(searchStr))
                    qq |= Q(item__NetWeigth=int(searchStr))
                    qq |= Q(item__TransNo=int(searchStr))
                    qq |= Q(item__VchNum=int(searchStr))

        if request.user.groups.filter(name="group_namayendgi_8_ostan").count() > 0:
            customers = SalesCustomerProfile.objects.filter(exp__namayandegi_8_ostaan=True)
            customers_codes = [customer.hamkaranCode + "    " if customer.hamkaranCode != None else "-1" for customer in
                               customers]
            # فیلتر تاریخش طوری باشد که بعد از اردیبهشت سال ۱۴۰۰ را بتواند ببیند
            dateof = datetime.strptime('2021-04-21', '%Y-%m-%d')
            self.queryset = self.queryset.filter(item__DLRef__in=customers_codes, item__VchDate__gte=dateof)

        self.queryset = self.queryset.filter(qq)

        result = super(ExitsViewSet, self).list(request, *args, **kwargs)
        if result.data.get("aaData"):
            for r in result.data.get("aaData"):
                try:
                    r["item"]["VchDate"] = mil_to_sh(r["item"]["VchDate"])
                except:
                    r["item"]["VchDate"] = "بدون تاریخ !"
        if result.data.get("results"):
            for r in result.data.get("results"):
                try:
                    r["item"]["VchDate"] = mil_to_sh(r["item"]["VchDate"])
                except:
                    r["item"]["VchDate"] = "بدون تاریخ !"
        # lst = super(ExitsViewSet, self).list(request, *args, **kwargs)
        for r in result.data.get("results"):
            r["hahScan"] = bool(ExtisFiles.objects.filter(VchHdrId=r['item']['VchHdrId']).count())
            r["hasSms"] = bool(ExitsSMS.objects.filter(VchHdrId=r['item']['VchHdrId']).count())
            r["readSms"] = bool(ExitsSMS.objects.filter(VchHdrId=r['item']['VchHdrId'], seenDate__nin=[None]).count())
            r['signCount'] = len(ExitsSigns.objects.filter(exitsLink=r["id"]).distinct("whichStep"))
            r["signTitle"] = self.get_sign_title(r['signCount'] + 1)

        return result

    def getHavaleKhoroojDetails(self, TransNo):
        pool = ConnectionPools.objects.get(name="AccInvTransTrace")
        sql = pool.sqls[0]["code"]
        sql = sql.replace("int__TransNo", str(TransNo))
        sql = sql.replace("<:", "")
        sql = sql.replace(":>", "")
        connection = Connections.objects.get(databaseName="sgdb")
        connection = ConnectionsViewSet().getConnection(connection)
        connection.execute(sql)
        sql_res = connection.fetchall()
        return sql_res

    @detail_route(methods=['GET'])
    def gotonext(self, request, *args, **kwargs):
        id = kwargs.get("id")
        fff = Exits.objects.filter(id__gt=id).order_by("id").first()
        if not fff:
            return Response({"id": ""})
        return Response({'id': str(fff.id)})

    @detail_route(methods=['GET'])
    def gotoprev(self, request, *args, **kwargs):
        id = kwargs.get("id")
        fff = Exits.objects.filter(id__lt=id).order_by("-id").first()
        if not fff:
            return Response({"id": ""})
        return Response({'id': str(fff.id)})

    @list_route(methods=["GET"])
    def getAggrList(self, request, *args, **kwargs):
        self.mapHamkaran()
        page = int(request.query_params.get('page'))
        search = request.query_params.get('search')
        startPoint = (page * 20) - 20
        endPoint = (page * 20)
        nextpage = page + 1
        prevpage = page - 1
        searchStr = request.query_params.get("search")
        qq = None
        if searchStr:
            if searchStr != "":
                qq = Q(item__Driver__icontains=searchStr)
                qq |= Q(item__RealTransNo__icontains=searchStr)
                qq |= Q(item__NationalCode__icontains=searchStr)
                qq |= Q(item__ZipCode__icontains=searchStr)
                qq |= Q(item__Phone__icontains=searchStr)
                qq |= Q(item__LicencNo__icontains=searchStr)
                qq |= Q(item__CntrprtName__icontains=searchStr)
                qq |= Q(item__CreatorName__icontains=searchStr)
                qq |= Q(item__TransCmpName__icontains=searchStr)
                qq |= Q(item__CarNumber__icontains=searchStr)
                if searchStr.isdigit():
                    qq |= Q(item__GrossWeigth=int(searchStr))
                    qq |= Q(item__NetWeigth=int(searchStr))
                    qq |= Q(item__TransNo=int(searchStr))
                    qq |= Q(item__VchNum=int(searchStr))

        lst = list(Exits.objects.filter(qq).aggregate(
            {
                "$group": {
                    "_id": "$item.TransNo",
                    "CntrprtName": {"$first": "$item.CntrprtName"},
                    "TransDate": {"$first": "$item.TransDate"},
                    "NetWeigth": {"$sum": "$item.NetWeigth"}
                }},
            {"$sort": {
                "TransDate": -1
            }
            },
            {"$skip": startPoint},
            {"$limit": endPoint}
        ))
        for r in lst:
            try:
                r["TransDate"] = mil_to_sh(r["TransDate"])

            except:
                r["TransDate"] = "بدون تاریخ !"

        for r in lst:
            r["hahScan"] = bool(ExtisFiles.objects.filter(transNo=r["_id"]).count())
            r["hasSms"] = bool(ExitsSMS.objects.filter(transNo=r["_id"]).count())
            r["readSms"] = bool(ExitsSMS.objects.filter(transNo=r["_id"], seenDate__nin=[None]).count())

        return Response({"data": lst, "nextpage": nextpage, "prevpage": prevpage})

    @detail_route(methods=["POST"])
    def makeItBatel(self, request, *args, **kwargs):
        exit = Exits.objects.get(id=kwargs['id'])
        signs = list(ExitsSigns.objects.filter(exitsLink=exit))
        codes = query(signs).distinct(lambda x: x.whichStep).select(lambda x: x.whichStep).to_list()

        groupName = "group_extis_permited_to_view_1"
        group = Group.objects.filter(name=groupName)
        if group.count() == 0:
            return Response({
                "errcode": 1,
                "msg": "گروه های عملیاتی توسط بهمنی ساخته نشده اند"
            })
            # raise Exception("1_" + groupName + " does not created Mohammad Please create it !")
        # user = MyUser.objects.get(id = positionInstance.userID)
        group = group[0]
        isAllowed = group.user_set.all().filter(id=request.user.id).count()

        if isAllowed == 0:
            raise Exception("شما مجوز ابطال ندارید")

        positionInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        if len(signs) < 2:
            itt = exit.item
            itt['itIsBatel'] = True
            itt['itIsBatelWhy'] = request.data['reason']
            itt['itIsBatelDatetime'] = datetime.now()
            itt['itIsBatelPositionID'] = positionInstance.positionID
            ess = ExitsSerializer(instance=exit, data={'item': itt})
            ess.is_valid(raise_exception=True)
            ess.save()
            return Response({'msg': 'ok'})

    @detail_route(methods=["GET"])
    def getDetailBarnamehSigns(self, request, *args, **kwargs):
        # getting signs
        exit = Exits.objects.get(id=kwargs['id'])
        signs = list(ExitsSigns.objects.filter(exitsLink=exit))
        codes = query(signs).distinct(lambda x: x.whichStep).select(lambda x: x.whichStep).to_list()
        ss = []
        for c in codes:
            current = query(signs).where(lambda x: x.whichStep == c).order_by_descending(
                lambda x: x.dateOfPost).to_list()
            if len(current) > 0:
                ss.append(current[0])
        # qrexit_ + exit_id + _ + positionID + _ +stepID
        if len(ss) > 0:
            signs = ExitsSignSerializer(instance=ss, many=True).data
            for s in signs:
                ps = PositionsDocument.objects.filter(positionID=s["positionID"]).order_by('-postDate')
                ps = ps[0]
                s["positionName"] = ps["profileName"]
                s["positionchartName"] = ps["chartName"]
                s["positionavatar"] = ps["avatar"]
                s["signCount"] = len(signs)
                s["dateOfPost"] = mil_to_sh_with_time(s["dateOfPost"])
                s["hash"] = "http://app.****.ir/SpecialApps/#!/home/Sales/kh/" + str(exit.id) + "/details"
                # s["hash"] = "http://app.****.ir/digital_sign/qrexit_" + str(exit.id) + "_" + str(ps.positionID) +
                #  "_" + str(s["whichStep"])
                del s["exitsLink"]
        return Response(signs)

    @detail_route(methods=["GET"])
    def getDetailBarnameh(self, request, *args, **kwargs):
        exit = Exits.objects.get(id=kwargs['id'])
        if exit.item["TransNo"] == None:
            return Response({})
        res = self.getHavaleKhoroojDetails(exit.item["TransNo"])
        for r in res:
            try:
                r["VchDate"] = mil_to_sh(r["VchDate"])
                r["TransDate"] = mil_to_sh(r["TransDate"])
            except:
                r["VchDate"] = "بدون تاریخ !"
                r["TransDate"] = "بدون تاریخ !"

        return Response(res)

    @detail_route(methods=["GET"])
    def getSMS(self, request, *args, **kwargs):
        smss = Exits.objects.get(id=kwargs['id'])
        exs = ExitsSigns.objects.filter(exitsLink=smss.id).order_by("-id").first()
        smss = ExitsSMS.objects.filter(VchHdrId=smss.item["VchHdrId"])
        smss = ExitsSMSSerializer(instance=smss, many=True).data
        for s in smss:
            if s.get("positionID"):
                positionInstance = PositionsDocument.objects.filter(positionID=s.get("positionID")).first()
                s["sendername"] = positionInstance.profileName
                s["senderchart"] = positionInstance.chartName
                s["dateOfPost"] = exs.dateOfPost if exs else None
        return Response(smss)

    @detail_route(methods=["GET"])
    def getFiles(self, request, *args, **kwargs):
        if kwargs.get("id") == None:
            return Response({})
        if kwargs.get("id") == "undefined":
            return Response({})

        smss = Exits.objects.get(id=kwargs['id'])
        lst = ExtisFiles.objects.filter(VchHdrId=smss.item["VchHdrId"])
        ser = ExtisFilesSerializer(instance=lst, many=True).data
        if len(ser) > 0:
            ser = ser[0]
        return Response(ser)

    @detail_route(methods=["POST"])
    def saveFiles(self, request, *args, **kwargs):
        VchHdrId = int(request.data["VchHdrId"])
        ExtisFiles.objects.filter(VchHdrId=VchHdrId).delete()
        ser = ExtisFilesSerializer(data={
            "Files": request.data["Files"],
            "VchHdrId": VchHdrId})
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @detail_route(methods=["POST"])
    def sendSms(self, request, *args, **kwargs):
        cells = request.data.get("mobile")
        if cells == None:
            inst = self.queryset.filter(item__VchHdrId=int(request.data.get("VchHdrId"))).first()
            # converting CustomerID to VchHdrId
            saleviewclass = SalesViewSet()
            customers = saleviewclass.getCustomers()
            customer = query(customers).where(
                lambda x: str(x['DLRef']).replace(' ', '') == inst['item']['DLRef'].replace(' ', '')).first()
            codeOf = customer['CstmrCode']

            instProf = SalesCustomerProfile.objects.filter(hamkaranCode=str(codeOf)).first()
            cells = instProf.exp['contact']['cell']

        for c in cells.split("-"):
            h = c.replace(" ", "")
            # generating link
            # -----------------------
            # -----------------------
            shortUID = uuid.uuid4().hex[:6].upper()
            cou = ExitsSMS.objects.filter(linkID=shortUID).count()
            if cou > 0:
                while True:
                    shortUID = uuid.uuid4().hex[:6].upper()
                    cou = ExitsSMS.objects.filter(linkID=shortUID).count()
                    if cou == 0:
                        break
            # -----------------------
            # -----------------------
            smms = request.data.get("sms").replace("::suid", shortUID).replace("  ", "")
            positionInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            sendSMS.delay(h, smms)
            dt = dict(

                VchHdrId=int(request.data.get("VchHdrId")),
                positionID=positionInstance.positionID,
                cellNoToSMS=h,
                # genID=cc.strResultMessage,
                # result=cc.SendSMS_SingleResult,
                genID="sent",
                result=False,
                msg=smms,
                linkID=shortUID
            )
            ser = ExitsSMSSerializer(data=dt)
            ser.is_valid(raise_exception=True)
            ser.save()

        return Response({})

    def template_view_showSignBodyPrc(self, request):
        return render_to_response('Sales/sign/signBody.html', {},
                                  context_instance=RequestContext(request))

    def template_view_Khoroj_Details(self, request):
        return render_to_response('Sales/Khorooj/details.html', {},
                                  context_instance=RequestContext(request))

    def template_view_Khoroj(self, request):
        return render_to_response('Sales/Khorooj/base.html', {},
                                  context_instance=RequestContext(request))
