import csv
import io
import pymssql
from datetime import datetime
import requests
import xlsxwriter
from asq.initiators import query
from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.decorators import list_route, detail_route
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Connections.models import ConnectionPools, Connections
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsViews import ConnectionsViewSet
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.ControlProject.permissions.ControlProjectBase import IsOwnerOrReadOnly_CostCol
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh_with_time, getCurrentYearShamsi
from amspApp.Infrustructures.Classes.MongoEngineSearchFilterBackend import MongoSearchFilter, FilterCompanyID
from amspApp.Infrustructures.Classes.convert_sqlresult_to_validstr import convert_sqlresultstr_to_valid_str
from amspApp.MyProfile.models import Profile
from amspApp.Sales.forms.profile import SaleCustomerFormDetailsFormV
from amspApp.Sales.models import SaleConversations, SaleConversationComments, SaleConversationItems, \
    SalesCustomerProfile, PishfactorsIgnore
from amspApp.Sales.permissions.basePermissions import CanCruidSale, IsHeSalePerson
from amspApp.Sales.serializers.SaleConversationSerializer import SaleConversationSerializer, \
    SaleConversationItemsSerializer
from amspApp._Share.ListPagination import DetailsPagination, ListObjectPaging
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset
from amspApp.tasks import sendSMS


class SalesViewSet(viewsets.ModelViewSet):
    pagination_class = DetailsPagination
    lookup_field = "id"
    serializer_class = SaleConversationSerializer
    queryset = SaleConversations.objects.all().order_by('-Open').order_by('-id')
    permission_classes = (IsOwnerOrReadOnly_CostCol, CanCruidSale,)
    filter_backends = (MongoSearchFilter, FilterCompanyID, OrderingFilter)
    search_fields = ("PrefactorID", "CustomerName", "HamkaranCode")
    trim = 16

    sqlserverIP = "172.16.5.10"
    sqlserverUsername = "rahsoon"
    sqlserverPassword = "****"
    sqlserverDBName = "sgdb"

    def checkPerm(self, req):
        if req.user.groups.filter(
                Q(name__contains="foroosh") |
                Q(name__contains="group_namayendgi_8_ostan") |
                Q(name__contains="ext")
        ).count() == 0:
            raise Exception("مجوز دسترسی ندارید")

    def initialize_request(self, request, *args, **kwargs):
        self.checkPerm(request)
        return super(SalesViewSet, self).initialize_request(request, *args, **kwargs)

    countries = [
        'Jolee',
        'Posco',
        'Tianjin',
        'SWKD',
        'Russia',
        'Shougang',
        'Commat',
        'Mobarake',
        'HaftAlmas',
        'FuladGharb',
        'DongChong',
        'BLXF',
        'Chon Yuen Tai',
        'fffff',
        'ttttt',
        'uyyyyyy',
        'uyyyyyy',
        'uyyyyyy',
        'uyyyyyy',
        'uyyyyyy',
        'uyyyyyy',
        'uyyyyyy',
        'uyyyyyy',
        'uyyyyyy',
        'uyyyyyy',
        'uyyyyyy',
        'uyyyyyy',
    ]

    def convertCodeToSep(self, code):

        keshavar = (code[2:3])
        if keshavar.isdigit():
            keshavar = int(keshavar)
        else:
            if keshavar == "A":
                keshavar = 10
            if keshavar == "B":
                keshavar = 11
            if keshavar == "C":
                keshavar = 12
            if keshavar == "D":
                keshavar = 13
            if keshavar == "E":
                keshavar = 14
            if keshavar == "F":
                keshavar = 15
            if keshavar == "G":
                keshavar = 16
            if keshavar == "H":
                keshavar = 17
            if keshavar == "I":
                keshavar = 18
            if keshavar == "J":
                keshavar = 19
            if keshavar == "L":
                keshavar = 20
            if keshavar == "Y":
                keshavar = 21

            if keshavar == "a":
                keshavar = 10
            if keshavar == "b":
                keshavar = 11
            if keshavar == "c":
                keshavar = 12
            if keshavar == "d":
                keshavar = 13
            if keshavar == "e":
                keshavar = 14
            if keshavar == "f":
                keshavar = 15
            if keshavar == "g":
                keshavar = 16
            if keshavar == "h":
                keshavar = 17
            if keshavar == "i":
                keshavar = 18
            if keshavar == "j":
                keshavar = 19
            if keshavar == "l":
                keshavar = 20
            if keshavar == "y":
                keshavar = 21

        dd = {}
        # try:

        try:
            dd = dict(
                noe=int(code[0:2]),
                keshvar=self.countries[keshavar],
                temper=int(code[3:4]),
                sath='Stone' if (code[4:5]) == "2" else "Bright",
                zekhamat=int(code[5:7]),
                arz=int(code[7:10]),
                keifiat=int(code[10:11]),
                tool=int(code[11:14], )
            )
        except:
            d = 1
        # except :
        #         #     d = 1
        #
        #         # try :
        #         #
        #         #     cc = dd
        #         # except:
        #         #     d = 1

        return dd

    def convertCodeToSepWithoutSpec(self, code):

        keshavar = (code[2:3])
        if keshavar.isdigit():
            keshavar = int(keshavar)
        else:
            if keshavar == "A":
                keshavar = 10
            if keshavar == "B":
                keshavar = 11
            if keshavar == "C":
                keshavar = 12
            if keshavar == "D":
                keshavar = 13
            if keshavar == "E":
                keshavar = 14
            if keshavar == "F":
                keshavar = 15

            if keshavar == "a":
                keshavar = 10
            if keshavar == "b":
                keshavar = 11
            if keshavar == "c":
                keshavar = 12
            if keshavar == "d":
                keshavar = 13
            if keshavar == "e":
                keshavar = 14
            if keshavar == "f":
                keshavar = 15

        return dict(
            keshvar=keshavar,
            temper=int(code[1:2]),
            sath='Stone' if (code[2:3]) == "2" else "Bright",
            zekhamat=int(code[3:5]),
            arz=int(code[5:8]),
            keifiat=int(code[8:9]))

    def isPartCodeAvailable(self, partCode, amount):
        return True

        currrentMojoodi = self.hamkaran_GetMojoodi()
        currrentMojoodi = query(currrentMojoodi).where(lambda x: x["PartCode"] == partCode).to_list()[0]
        # getting mojoodi conv
        convs = SaleConversations.objects.filter(Open=True, PrefactorID__exists=False)
        convItems = SaleConversationItems.objects.filter(
            saleConversationLink__in=[str(c.id) for c in convs], itemID=currrentMojoodi["PartCode"])
        sumOfConv = convItems.sum("amount")
        sumOfHamran = currrentMojoodi["sumOf"] - (currrentMojoodi["sumPish"] + currrentMojoodi["sumPishOK"])

        totalSum = sumOfHamran - sumOfConv

        if totalSum < amount:
            # return False
            return True

        return True

    def GetAmountOfAvailablePartCode(self, partCode):
        currrentMojoodi = self.hamkaran_GetMojoodi()
        currrentMojoodi = query(currrentMojoodi).where(lambda x: x["PartCode"] == partCode).to_list()[0]
        # getting mojoodi conv
        convs = SaleConversations.objects.filter(Open=True, PrefactorID__exists=False)
        convItems = SaleConversationItems.objects.filter(
            saleConversationLink__in=[str(c.id) for c in convs], itemID=currrentMojoodi["PartCode"])
        sumOfConv = convItems.sum("amount")
        sumOfHamran = currrentMojoodi["sumOf"] - (currrentMojoodi["sumPish"] + currrentMojoodi["sumPishOK"])

        totalSum = sumOfHamran - sumOfConv

        return totalSum

    def getInCacheNoAuth(self):
        # currrentMojoodi = self.hamkaran_GetMojoodi()
        # extracting mojoodi from text
        # countries
        # for c in currrentMojoodi:
        #     dd = self.convertCodeToSep(c["PartCode"])
        #     c.update(dd)
        # cache.set("mojoodii_" + str(request.user.id), currrentMojoodi, 20)

        currrentCardex = self.hamkaran_GetCardex()

        currrentPish = self.hamkaran_GetOpenPish()

        for c in currrentCardex:
            c.update(self.convertCodeToSep(c["PartCode"]))

        # updating foolad mobarakeh if == 66 then minus 20
        for c in currrentCardex:
            if c['keshvar'] == 'Mobarake' and c['noe'] == 66:
                c['arz'] = c['arz'] - self.trim

        for c in currrentPish:
            c.update(self.convertCodeToSep(c["PartCode"]))
            # c['arzAfterTrim'] = c['arz']
            # if c['keshvar'] == 'Mobarake':
            #     c['arz'] = c['arz'] + 20
            #     c['PartCode'] = c['PartCode'][0:7] + str(c['arz']) + c['PartCode'][11:15]

        # posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        convs = SaleConversations.objects.filter(Open=True, PrefactorID__exists=False)
        convItems = SaleConversationItems.objects.filter(saleConversationLink__in=[str(c.id) for c in convs])
        convItems = SaleConversationItemsSerializer(instance=convItems, many=True).data

        for c in convItems:
            c.update(self.convertCodeToSep(c["itemID"]))

        cardexGroup = query(currrentCardex).group_by(lambda x: x['PartCode'][2:11],
                                                     result_selector=lambda key, group:
                                                     {
                                                         'PartCode': key,
                                                         'qty': group.sum(lambda x: x['XQtyRatio']),
                                                         'details': group.group_by(lambda x: x['noe'],
                                                                                   result_selector=lambda xkey, xgroup:
                                                                                   {
                                                                                       'noe': xkey,
                                                                                       'qty': xgroup.sum(
                                                                                           lambda x: x["XQtyRatio"]),
                                                                                       'details': xgroup.group_by(
                                                                                           lambda x: x['tool'],
                                                                                           result_selector=lambda xkey,
                                                                                                                  xgroup: {
                                                                                               'tool': xkey,
                                                                                               'qty': xgroup.sum(
                                                                                                   lambda x: x[
                                                                                                       'XQtyRatio'])
                                                                                           }
                                                                                       ).to_list()
                                                                                   }
                                                                                   ).to_list()
                                                     }).order_by_descending(lambda x: x['qty']).to_list()

        pishGroup = query(currrentPish).where(lambda x: x['isAccountable'] == True).group_by(
            lambda x: x['PartCode'][2:11],
            result_selector=lambda key, group: {
                'PartCode': key,
                'qtyPish': group.sum(lambda x: x['Qty']),
                'Pishs': group.group_by(lambda x: x['noe'],
                                        result_selector=lambda key, group: {
                                            'noe': key,
                                            'qty': group.sum(lambda x: x['Qty']),
                                            'details': group.group_by(
                                                lambda x: x['tool'],
                                                result_selector=lambda
                                                    key, group: {
                                                    'tool': key,
                                                    'qty': group.sum(
                                                        lambda x: x[
                                                            'Qty'])
                                                }).to_list()
                                        }).to_list()
            }).order_by_descending(lambda x: x['qtyPish']).to_list()
        convGroup = query(convItems).group_by(lambda x: x['itemID'][2:11],
                                              result_selector=lambda key, group: {
                                                  'PartCode': key,
                                                  'qtyConv': group.sum(lambda x: x['amount']),
                                                  'Convs': group.group_by(lambda x: x['noe'],
                                                                          result_selector=lambda key, group: {
                                                                              'noe': key,
                                                                              'qty': group.sum(lambda x: x['amount']),
                                                                              'details': group.group_by(
                                                                                  lambda x: x['tool'],
                                                                                  result_selector=lambda
                                                                                      key, group: {
                                                                                      'tool': key,
                                                                                      'qty': group.sum(
                                                                                          lambda x: x[
                                                                                              'amount'])
                                                                                  }).to_list()
                                                                          }).to_list()
                                              }).order_by_descending(lambda x: x['qtyConv']).to_list()

        for c in cardexGroup:
            for p in pishGroup:
                if c["PartCode"] == p["PartCode"]:
                    c.update(p)

            for p in convGroup:
                if c["PartCode"] == p["PartCode"]:
                    c.update(p)

            c['total'] = c['qty'] - c['qtyPish'] if 'qtyPish' in c else c['qty']
            c['total'] = c['total'] - c['qtyConv'] if 'qtyConv' in c else c['total']
            if not "qtyPish" in c:
                c["qtyPish"] = 0
            if not "qtyConv" in c:
                c["qtyConv"] = 0
            c.update(self.convertCodeToSepWithoutSpec(c['PartCode']))

            # c['arzAfterTrim'] = c['arz']

        # cache.set("currentCardex_" + str(request.user.id), currrentCardex, 200)
        cache.set("currentCardexGroup_csv", cardexGroup, 200)

        # url = 'http://docs.google.com/spreadsheets/d/121JRV4dh0yaUdT2kmXpSdc3ymWNnUcWtMi_XP92Xn4Q/pub?output=csv'
        # with requests.Session() as s:
        #     download = s.get(url)
        #     decoded_content = download.content.decode('utf-8')
        #     cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        #     mylist = list(cr)
        #     cache.set("mojoodii_" + str(request.user.id), mylist, 600)
        #     s.close()

        url = 'http://docs.google.com/spreadsheets/d/1oV-anFgdaH8QYBWYa8vGsG0aDBi65Uqq_Rfv_yqr4yY/pub?gid=0&single=true&output=csv'
        with requests.Session() as s:
            download = s.get(url)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            mylist = list(cr)
            cache.set("future_csv", mylist, 600)
            s.close()

    def getInCache(self, request):
        # currrentMojoodi = self.hamkaran_GetMojoodi()
        # extracting mojoodi from text
        # countries
        # for c in currrentMojoodi:
        #     dd = self.convertCodeToSep(c["PartCode"])
        #     c.update(dd)
        # cache.set("mojoodii_" + str(request.user.id), currrentMojoodi, 20)

        currrentCardex = self.hamkaran_GetCardex()

        currrentPish = self.hamkaran_GetOpenPish()

        for c in currrentCardex:
            c.update(self.convertCodeToSep(c["PartCode"]))

        # updating foolad mobarakeh if == 66 then minus 20
        for c in currrentCardex:
            if c['keshvar'] == 'Mobarake' and c['noe'] == 66:
                c['arz'] = c['arz'] - self.trim

        for c in currrentPish:
            c.update(self.convertCodeToSep(c["PartCode"]))
            # c['arzAfterTrim'] = c['arz']
            # if c['keshvar'] == 'Mobarake':
            #     c['arz'] = c['arz'] + 20
            #     c['PartCode'] = c['PartCode'][0:7] + str(c['arz']) + c['PartCode'][11:15]

        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        convs = SaleConversations.objects.filter(Open=True, PrefactorID__exists=False)
        convItems = SaleConversationItems.objects.filter(companyID=posiIns.companyID,
                                                         saleConversationLink__in=[str(c.id) for c in convs])
        convItems = SaleConversationItemsSerializer(instance=convItems, many=True).data

        for c in convItems:
            c.update(self.convertCodeToSep(c["itemID"]))

        cardexGroup = query(currrentCardex).group_by(lambda x: x['PartCode'][2:11],
                                                     result_selector=lambda key, group:
                                                     {
                                                         'PartCode': key,
                                                         'qty': group.sum(lambda x: x['XQtyRatio']),
                                                         'details': group.group_by(lambda x: x['noe'],
                                                                                   result_selector=lambda xkey, xgroup:
                                                                                   {
                                                                                       'noe': xkey,
                                                                                       'qty': xgroup.sum(
                                                                                           lambda x: x["XQtyRatio"]),
                                                                                       'details': xgroup.group_by(
                                                                                           lambda x: x['tool'],
                                                                                           result_selector=lambda xkey,
                                                                                                                  xgroup: {
                                                                                               'tool': xkey,
                                                                                               'qty': xgroup.sum(
                                                                                                   lambda x: x[
                                                                                                       'XQtyRatio'])
                                                                                           }
                                                                                       ).to_list()
                                                                                   }
                                                                                   ).to_list()
                                                     }).order_by_descending(lambda x: x['qty']).to_list()

        pishGroup = query(currrentPish).where(lambda x: x['isAccountable'] == True).group_by(
            lambda x: x['PartCode'][2:11],
            result_selector=lambda key, group: {
                'PartCode': key,
                'qtyPish': group.sum(lambda x: x['Qty']),
                'Pishs': group.group_by(lambda x: x['noe'],
                                        result_selector=lambda key, group: {
                                            'noe': key,
                                            'qty': group.sum(lambda x: x['Qty']),
                                            'details': group.group_by(
                                                lambda x: x['tool'],
                                                result_selector=lambda
                                                    key, group: {
                                                    'tool': key,
                                                    'qty': group.sum(
                                                        lambda x: x[
                                                            'Qty'])
                                                }).to_list()
                                        }).to_list()
            }).order_by_descending(lambda x: x['qtyPish']).to_list()
        convGroup = query(convItems).group_by(lambda x: x['itemID'][2:11],
                                              result_selector=lambda key, group: {
                                                  'PartCode': key,
                                                  'qtyConv': group.sum(lambda x: x['amount']),
                                                  'Convs': group.group_by(lambda x: x['noe'],
                                                                          result_selector=lambda key, group: {
                                                                              'noe': key,
                                                                              'qty': group.sum(lambda x: x['amount']),
                                                                              'details': group.group_by(
                                                                                  lambda x: x['tool'],
                                                                                  result_selector=lambda
                                                                                      key, group: {
                                                                                      'tool': key,
                                                                                      'qty': group.sum(
                                                                                          lambda x: x[
                                                                                              'amount'])
                                                                                  }).to_list()
                                                                          }).to_list()
                                              }).order_by_descending(lambda x: x['qtyConv']).to_list()

        for c in cardexGroup:
            for p in pishGroup:
                if c["PartCode"] == p["PartCode"]:
                    c.update(p)

            for p in convGroup:
                if c["PartCode"] == p["PartCode"]:
                    c.update(p)

            c['total'] = c['qty'] - c['qtyPish'] if 'qtyPish' in c else c['qty']
            c['total'] = c['total'] - c['qtyConv'] if 'qtyConv' in c else c['total']
            if not "qtyPish" in c:
                c["qtyPish"] = 0
            if not "qtyConv" in c:
                c["qtyConv"] = 0
            c.update(self.convertCodeToSepWithoutSpec(c['PartCode']))

            # c['arzAfterTrim'] = c['arz']

        # cache.set("currentCardex_" + str(request.user.id), currrentCardex, 200)
        cache.set("currentCardexGroup_" + str(request.user.id), cardexGroup, 200)

        # url = 'http://docs.google.com/spreadsheets/d/121JRV4dh0yaUdT2kmXpSdc3ymWNnUcWtMi_XP92Xn4Q/pub?output=csv'
        # with requests.Session() as s:
        #     download = s.get(url)
        #     decoded_content = download.content.decode('utf-8')
        #     cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        #     mylist = list(cr)
        #     cache.set("mojoodii_" + str(request.user.id), mylist, 600)
        #     s.close()

        url = 'https://docs.google.com/spreadsheets/d/1oV-anFgdaH8QYBWYa8vGsG0aDBi65Uqq_Rfv_yqr4yY/pub?gid=0&single=true&output=csv'
        with requests.Session() as s:
            download = s.get(url)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            mylist = list(cr)
            cache.set("future_" + str(request.user.id), mylist, 600)
            s.close()

    @list_route(methods=["GET"])
    def refreshCache(self, request, *args, **kwargs):
        self.getInCache(request)
        return Response({"msg": "ok"})

    def checkInt(self, var):
        try:
            if type(var) == int:
                return var
            if type(var) == float:
                return int(var)

            if var.isdigit():
                return int(var)
            if var == "":
                return 0
        except:
            return 0
        return 0

    @list_route(methods=["POST"])
    def IgnorePish(self, request, *args, **kwargs):
        dt = dict(
            positionID=request.data['positionID'],
            companyID=request.data['companyID'],
            CstmrCode=request.data['details']['CstmrCode'],
            VchItmId=request.data['details']['VchItmId'],
            VchHdrRef=request.data['details']['VchHdrRef'],
            PartRef=request.data['details']['PartRef'],
            VchNo=request.data['details']['VchNo'],
        )
        PishfactorsIgnore.objects.filter(**dt).delete()
        if request.data['isAccountable']:
            PishfactorsIgnore(**dt).save()

        return Response({"msg": "ok"})

    @list_route(methods=["POST"])
    def getCardex(self, request, *args, **kwargs):
        data = request.data

        sql = """
            select top 9930
                CASE
                when (SUBSTRING(prt.PartCode, 1, 2) in ('66') and SUBSTRING(prt.PartCode, 3, 1) in ('7'))
                then stuff(prt.PartCode,8,3, cast(cast(SUBSTRING(prt.PartCode, 8, 3) as INT)-%d as NVARCHAR(3) )) else prt.PartCode end as [PartCode],
                prt.PartName,
                vsf.VchItmId,
                vsf.XQtyRatio,
                vsf.XDate,
                '13'+ REPLACE(gnr.sgfn_DateToShamsiDate(vsf.XDate), '/','/')  as [shamsi],
                vsf.DsVchDesc
                from
                  [sgdb].[inv].[vwCardex3]  vsf
                  inner join [sgdb].[inv].[Part] prt on vsf.PartRef = prt.Serial

                  where
                  SUBSTRING(prt.PartCode, 1, 2) in ('66','77','88')
                  and
                  SUBSTRING(prt.PartCode, 5, 6) not in('000000')
                  and
                  VchDate between '2019-03-21' and '2020-03-21'
                  AND
                  prt.PartCode = '%02d%s%03d'

                  order by XDate
        """ % (
            self.trim,
            data["noe"],
            data["partCode"],
            data["tool"],
        )

        conn = pymssql.connect(self.sqlserverIP, self.sqlserverUsername, self.sqlserverPassword,
                               self.sqlserverDBName, charset="UTF-8", as_dict=True)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()

        # getting aggr
        sum = 0
        for r in result:
            if sum == 0:
                sum = r["XQtyRatio"]
            else:
                sum += r["XQtyRatio"]
            r["sum"] = sum

        return Response(
            dict(results=result)
        )

    @list_route(methods=["POST"])
    def getPishLevel3(self, request, *args, **kwargs):
        data = request.data

        sql = """
                select
                prt.PartCode,

                       SUBSTRING(prt.PartCode, 1, 2) as [noe],
                       SUBSTRING(prt.PartCode, 3, 1) as [keifiat],
                       SUBSTRING(prt.PartCode, 4, 1) as [temper],
                       SUBSTRING(prt.PartCode, 5, 1) as [sath],
                       SUBSTRING(prt.PartCode, 6, 2) as [zekhamat],
                       SUBSTRING(prt.PartCode, 8, 3) as [arz],
                       SUBSTRING(prt.PartCode, 11, 1) as [darajeh],
                       SUBSTRING(prt.PartCode, 12, 3) as [tool],

                prt.PartName,
                www.*

                from [sgdb].[sle].[vwSLERepPreFact] www
                inner join [sgdb].[inv].[Part] prt on www.PartRef = prt.Serial
                where

                   	   www.HStatus in (0,1)  and
                       SUBSTRING(prt.PartCode, 1, 2) ='%s' and
                       SUBSTRING(prt.PartCode, 4, 1) ='%s' and
                       SUBSTRING(prt.PartCode, 5, 1) ='%s' and
                       SUBSTRING(prt.PartCode, 6, 2) ='%s' and
                       SUBSTRING(prt.PartCode, 8, 3) ='%s' and
                       SUBSTRING(prt.PartCode, 12, 3) ='%03d'

                                       /*
                 *     SUBSTRING(prt.PartCode, 1, 2) as [sharh], +++
                       SUBSTRING(prt.PartCode, 3, 1) as [BP],
                       SUBSTRING(prt.PartCode, 4, 1) as [TEMPER],+++
                       SUBSTRING(prt.PartCode, 5, 1) as [sath],+++
                       SUBSTRING(prt.PartCode, 6, 2) as [zekhamat],+++
                       SUBSTRING(prt.PartCode, 8, 3) as [arz],+++
                       SUBSTRING(prt.PartCode, 11, 1) as [darajeh],
                       SUBSTRING(prt.PartCode, 12, 3) as [tool],+++
                 * */

        """ % (
            data["noe"],
            data["temper"],
            "1" if data["sath"] == "Bright" else "2",
            data["zekhamat"],
            data["arz"],
            data["tool"],
        )

        conn = pymssql.connect(self.sqlserverIP, self.sqlserverUsername, self.sqlserverPassword,
                               self.sqlserverDBName, charset="UTF-8", as_dict=True)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()

        # getting aggr
        for r in result:
            filter = dict(
                CstmrCode=r['CstmrCode'],
                VchItmId=r['VchItmId'],
                VchHdrRef=r['VchHdrRef'],
                PartRef=r['PartRef'],
                VchNo=r['VchNo'],
            )
            pishCount = PishfactorsIgnore.objects.filter(**filter)
            r["isAccountable"] = True if pishCount.count() == 0 else False
            if r["isAccountable"] == False:
                posIns = PositionsDocument.objects.filter(positionID=pishCount[0].positionID)[0]
                r["isAccDetails"] = dict(
                    chartName=posIns.chartName,
                    profileName=posIns.profileName,
                    avatar=posIns.avatar,
                    dateOfPost=pishCount[0].dateOfPost)

        return Response(dict(results=result))

    @list_route(methods=["POST"])
    def getConvLevel3(self, request, *args, **kwargs):
        filterTxt = "%2d%s%03d" % (
            request.data['noe'], request.data['details']['item']['PartCode'], request.data['tool'])
        convs = SaleConversationItems.objects.filter(itemID=filterTxt)
        convs = list(convs)
        convsParent = [x.saleConversationLink for x in list(convs)]
        convsParent = query(convsParent).where(lambda x: hasattr(x, 'CustomerID')).where(
            lambda x: x.Open == True).where(lambda x: x.PrefactorID == None).to_list()

        convs = SaleConversationItems.objects.filter(itemID=filterTxt, saleConversationLink__in=convsParent)
        convs = list(convs)
        # generating out puts
        """
CstmrName
PartCode
PartName
Qty
PreFactPrice
PreFactPrice
PreFactTotalPrice
        """
        outPut = {}
        outPut["results"] = []
        for c in convs:
            posIns = PositionsDocument.objects.filter(positionID=c.positionID)[0]
            debugging = c.saleConversationLink.id
            if hasattr(c.saleConversationLink, 'CustomerName'):
                det = dict(
                    CstmrName=c.saleConversationLink.CustomerName,
                    ConvID=str(c.saleConversationLink.id),
                    PartCode=c.itemID,
                    PartName=c.itemName,
                    Qty=c.amount,
                    Price=c.fee,
                    TotalPrice=c.amount * c.fee,
                    howPay=c.paymentType,
                    details=dict(
                        chartName=posIns.chartName,
                        profileName=posIns.profileName,
                        avatar=posIns.avatar, ),
                    dateOfPost=c.dateOfPost
                )
                outPut["results"].append(det)

        return Response(outPut)

    @list_route(methods=["GET"])
    def getMojoodiExcel(self, request, *args, **kwargs):
        kwargs["isItExcel"] = True
        result = self.getMojoodies(request, *args, **kwargs)
        res = []

        for r in result:
            p = {}
            p["MojoodiForoosh"] = r["total"]
            p["PartCode"] = r["PartCode"]
            p["keifiat"] = r["keifiat"]
            p["keshvar"] = r["keshvar"]
            p["sath"] = r["sath"]
            p["temper"] = r["temper"]
            p["arz"] = r["arz"]
            p["zekhamat"] = r["zekhamat"]
            p["anbar"] = r["qty"]
            p["qtyPish"] = r["qtyPish"]
            p["qtyConv"] = r["qtyConv"]

            res.append(p)

        output = io.BytesIO()
        # fileAddr = os.path.join(tmpdir, 'excel.xlsx')

        workbook = xlsxwriter.Workbook(output)

        fontFormat = workbook.add_format({"font_name": "B Nazanin"})
        mySheet = workbook.add_worksheet("DBTable")
        mySheet.is_right_to_left = True

        bold = workbook.add_format({'bold': True, "font_name": "B Nazanin"})
        simple = workbook.add_format({'bold': False, "font_name": "B Nazanin"})

        # worksheet = workbook.add_worksheet()

        row = 0
        col = 0

        # first rows
        rr = 0
        for cc in res[0].keys():
            mySheet.write(0, rr, cc, bold)
            rr += 1

        row = 1
        for r in res:
            rr = 0
            for cc in r.keys():
                mySheet.write(row, rr, r[cc], simple)
                rr += 1
            row += 1

        workbook.close()

        output.seek(0)

        dt = datetime.now()
        dt = mil_to_sh_with_time(dt).replace("/", "_").replace(" ", "__").replace(":", "_")

        response = HttpResponse(output,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s' % (dt + ".xlsx")
        return response

    # @list_route(methods=["GET"])
    # @permission_classes([AllAccess])
    # @authentication_classes([AllowAny])
    # @csrf_exempt
    # def getMojoodiCsv(self, request, *args, **kwargs):
    #     kwargs["isItExcel"] = True
    #     result = self.getMojoodiesNoAuth(request, *args, **kwargs)
    #     res = []
    #
    #     for r in result:
    #         p = {}
    #         p["MojoodiForoosh"] = r["total"]
    #         p["PartCode"] = r["PartCode"]
    #         p["keifiat"] = r["keifiat"]
    #         p["keshvar"] = r["keshvar"]
    #         p["sath"] = r["sath"]
    #         p["temper"] = r["temper"]
    #         p["arz"] = r["arz"]
    #         p["zekhamat"] = r["zekhamat"]
    #         p["anbar"] = r["qty"]
    #         p["qtyPish"] = r["qtyPish"]
    #         p["qtyConv"] = r["qtyConv"]
    #
    #         res.append(p)
    #
    #     # vv = dicttoxml(res, custom_root='test', attr_type=False)
    #     if len(res) == 0:
    #         return Response({})
    #
    #     headings = list(res[0].keys())
    #
    #     def generateGuidName():
    #         return uuid.uuid4().hex + uuid.uuid4().hex
    #
    #     decodeName = generateGuidName()
    #     temp_file = os.path.join(tempfile.gettempdir(), 'tmp_' + decodeName + '_insecure.tmp')
    #     with open(temp_file, "w", newline="") as output_file:
    #         dict_writer = csv.DictWriter(output_file, headings)
    #         dict_writer.writeheader()
    #         dict_writer.writerows(res)
    #
    #
    #
    #     # with open(temp_file,'w', newline='') as myCSVFile:
    #     #     csvWriter = csv.writer(myCSVFile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
    #     #     csvWriter.writerow(headings)
    #     #     for data in res:
    #     #         csvWriter.writerow(data)
    #
    #
    #
    #
    #     # output = io.BytesIO()
    #     # fileAddr = os.path.join(tmpdir, 'excel.xlsx')
    #
    #     resp = HttpResponse('')
    #     with open(temp_file, 'r') as tmp:
    #         filename = tmp.name.split('/')[-1]
    #         resp = HttpResponse(tmp, content_type='text/csv;charset=UTF-8')
    #         resp['Content-Disposition'] = "attachment; filename=bahmany.csv"
    #
    #     return resp

    @list_route(methods=["POST"])
    def getMojoodies(self, request, *args, **kwargs):

        if request.user.groups.filter(name='foroosh').count() == 0:
            return Response({})

        # important Updating Trimsssss !!!
        data = cache.get('currentCardexGroup_' + str(request.user.id))
        if not data:
            self.getInCache(request)
            data = cache.get('currentCardexGroup_' + str(request.user.id))

        filter = request.data
        params = request.query_params

        if params.get("sort"):
            sorts = params["sort"].split(",")
            for s in sorts:

                if s == "Mojoodi":
                    data = query(data).order_by(lambda x: x["total"]).to_list()
                if s == "-Mojoodi":
                    data = query(data).order_by_descending(lambda x: x["total"]).to_list()

                if s == "temper":
                    data = query(data).order_by(lambda x: x["temper"]).to_list()
                if s == "-temper":
                    data = query(data).order_by_descending(lambda x: x["temper"]).to_list()

                if s == "zekhamat":
                    data = query(data).order_by(lambda x: x["zekhamat"]).to_list()
                if s == "-zekhamat":
                    data = query(data).order_by_descending(lambda x: x["zekhamat"]).to_list()

                if s == "keifiat":
                    data = query(data).order_by(lambda x: x["keifiat"]).to_list()
                if s == "-keifiat":
                    data = query(data).order_by_descending(lambda x: x["keifiat"]).to_list()

                if s == "keshvar":
                    data = query(data).order_by(lambda x: x["keshvar"]).to_list()
                if s == "-keshvar":
                    data = query(data).order_by_descending(lambda x: x["keshvar"]).to_list()

                if s == "arz":
                    data = query(data).order_by(lambda x: x["arz"]).to_list()
                if s == "-arz":
                    data = query(data).order_by_descending(lambda x: x["arz"]).to_list()

                if s == "sath":
                    data = query(data).order_by(lambda x: x["sath"]).to_list()
                if s == "-sath":
                    data = query(data).order_by_descending(lambda x: x["sath"]).to_list()

                if s == "anbar":
                    data = query(data).order_by(lambda x: x["qty"]).to_list()
                if s == "-anbar":
                    data = query(data).order_by_descending(lambda x: x["qty"]).to_list()

                if s == "pish":
                    data = query(data).order_by(lambda x: x["qtyPish"]).to_list()
                if s == "-pish":
                    data = query(data).order_by_descending(lambda x: x["qtyPish"]).to_list()

                if s == "conv":
                    data = query(data).order_by(lambda x: x["qtyConv"]).to_list()
                if s == "-conv":
                    data = query(data).order_by_descending(lambda x: x["qtyConv"]).to_list()

        # data = self.get

        # data = data.where(lambda x: len(x[0]) > 2)
        # for pp in [["temper", 1], ["tool", 6], ["zekhamat", 3], ["arz", 4]]:

        if filter.get("temper"):
            if filter["temper"] > 0:
                data = query(data).where(
                    lambda x: self.checkInt(x["temper"]) <= filter["temper"] + filter["temper_tolerance"]
                              and self.checkInt(x["temper"]) >= filter["temper"] - filter["temper_tolerance"]).to_list()

        if filter.get("tool"):
            if filter["tool"] > 0:
                data = query(data).where(
                    lambda x: self.checkInt(x["tool"]) <= filter["tool"] + filter["tool_tolerance"]
                              and self.checkInt(x["tool"]) >= filter["tool"] - filter["tool_tolerance"]).to_list()

        if filter.get("zekhamat"):
            if filter["zekhamat"] > 0:
                data = query(data).where(
                    lambda x: self.checkInt(x["zekhamat"]) <= filter["zekhamat"] + filter["zekhamat_tolerance"]
                              and self.checkInt(x["zekhamat"]) >= filter["zekhamat"] - filter[
                                  "zekhamat_tolerance"]).to_list()

        if filter.get("arz"):
            if filter["arz"] > 0:
                data = query(data).where(
                    lambda x: self.checkInt(x["arz"]) <= filter["arz"] + filter["arz_tolerance"]
                              and self.checkInt(x["arz"]) >= filter["arz"] - filter["arz_tolerance"]).to_list()

        if "sath" in filter:
            if not (str(filter["sath"]).isdigit()):
                data = query(data).where(
                    lambda x: x["sath"] == filter["sath"]
                ).to_list()

        for f in data:
            if f.get("noe") == "66": f["noestr"] = "ورق سیاه"
            if f.get("noe") == "77": f["noestr"] = "کویل"
            if f.get("noe") == "88": f["noestr"] = "برش خورده"

        # getting totals
        saleTotal = 0
        anbarTotal = 0
        pishTotal = 0
        convTotal = 0
        saleTotal = query(data).sum(lambda x: x["total"])
        anbarTotal = query(data).sum(lambda x: x["qty"])
        pishTotal = query(data).sum(lambda x: x["qtyPish"])
        convTotal = query(data).sum(lambda x: x["qtyConv"])

        params = request.query_params
        page = 0
        if 'page' in params:
            page = int(params["page"]) - 1

        page_size = 20
        if 'page_size' in params:
            page_size = int(params["page_size"])

        page_len = int(len(data) / page_size)
        if kwargs.get("isItExcel") == True:
            return data

        result = list(ListObjectPaging().paginate(data, page_size))[page] if len(data) > 0 else []

        return Response({
            "totals":
                dict(
                    saleTotal=saleTotal,
                    anbarTotal=anbarTotal,
                    pishTotal=pishTotal,
                    convTotal=convTotal),
            "msg": "ok",
            "results": result,
            'page': page + 1,
            'page_count': page_len,
            'count': len(data),
            'page_size': page_size})

    def getMojoodiesNoAuth(self, request):

        # important Updating Trimsssss !!!
        data = cache.get('currentCardexGroup_csv')
        if not data:
            self.getInCacheNoAuth()
            data = cache.get('currentCardexGroup_csv')

        for f in data:
            if f.get("noe") == "66": f["noestr"] = "ورق سیاه"
            if f.get("noe") == "77": f["noestr"] = "کویل"
            if f.get("noe") == "88": f["noestr"] = "برش خورده"

        # getting totals
        saleTotal = 0
        anbarTotal = 0
        pishTotal = 0
        convTotal = 0
        saleTotal = query(data).sum(lambda x: x["total"])
        anbarTotal = query(data).sum(lambda x: x["qty"])
        pishTotal = query(data).sum(lambda x: x["qtyPish"])
        convTotal = query(data).sum(lambda x: x["qtyConv"])

        params = {}
        page = 0
        if 'page' in params:
            page = int(params["page"]) - 1

        page_size = 20000000
        if 'page_size' in params:
            page_size = int(params["page_size"])

        page_len = int(len(data) / page_size)

        result = list(ListObjectPaging().paginate(data, page_size))[page] if len(data) > 0 else []

        return Response({
            "totals":
                dict(
                    saleTotal=saleTotal,
                    anbarTotal=anbarTotal,
                    pishTotal=pishTotal,
                    convTotal=convTotal),
            "msg": "ok",
            "results": result,
            'page': page + 1,
            'page_count': page_len,
            'count': len(data),
            'page_size': page_size})

    @list_route(methods=["POST"])
    def getFutures(self, request, *args, **kwargs):
        return Response({})
        mylist = cache.get("future_" + str(request.user.id))
        if not mylist:
            self.getInCache(request)
            mylist = cache.get("future_" + str(request.user.id))

        # converting
        # converting temper / zekhamat / arz / tool /kilos to int

        mylist = mylist[1::]
        for m in mylist:
            for i in range(0, 15):
                m[i] = int(m[i].replace(",", "")) if m[i].replace(",", "").isdigit() else m[i]
        # -----------------------------------------

        filter = request.data
        data = query(mylist)
        data = data.where(lambda x: len(x[0]) > 2)
        # for pp in [["temper", 1], ["tool", 6], ["zekhamat", 3], ["arz", 4]]:
        if filter.get("temper"):
            if filter["temper"] > 0:
                data = data.where(
                    lambda x: self.checkInt(x[1]) <= filter["temper"] + filter["temper_tolerance"]
                              and self.checkInt(x[1]) >= filter["temper"] - filter["temper_tolerance"])

        if filter.get("tool"):
            if filter["tool"] > 0:
                data = data.where(
                    lambda x: self.checkInt(x[6]) <= filter["tool"] + filter["tool_tolerance"]
                              and self.checkInt(x[6]) >= filter["tool"] - filter["tool_tolerance"])

        if filter.get("zekhamat"):
            if filter["zekhamat"] > 0:
                data = data.where(
                    lambda x: self.checkInt(x[3]) <= filter["zekhamat"] + filter["zekhamat_tolerance"]
                              and self.checkInt(x[3]) >= filter["zekhamat"] - filter["zekhamat_tolerance"])

        if filter.get("arz"):
            if filter["arz"] > 0:
                data = data.where(
                    lambda x: self.checkInt(x[4]) <= filter["arz"] + filter["arz_tolerance"]
                              and self.checkInt(x[4]) >= filter["arz"] - filter["arz_tolerance"])

        if "sath" in filter:
            if not (str(filter["sath"]).isdigit()):
                data = data.where(
                    lambda x: x[2] == filter["sath"]
                )

        return Response({"msg": "ok", "results": data.to_list()})

    def get_queryset(self):
        if "filter" in self.request.query_params:
            qr = self.request.query_params["filter"].split("-")
            if qr[0] == 'true' and qr[1] == 'false':
                self.queryset = self.queryset.filter(Open=True)
            if qr[1] == 'true' and qr[0] == 'false':
                self.queryset = self.queryset.filter(Open=False)
            if qr[2] == 'true' and qr[3] == 'false':
                self.queryset = self.queryset.filter(PrefactorID__ne=None)
            if qr[2] == 'false' and qr[3] == 'true':
                self.queryset = self.queryset.filter(PrefactorID=None)
        return super(SalesViewSet, self).get_queryset()

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = posiIns.positionID
            request.data["companyID"] = posiIns.companyID
            request.data["positionID"] = posiIns.positionID
            if not "CustomerID" in request.data:
                request.data["CustomerIsInAccounting"] = False
            else:
                if request.data["CustomerID"] == "":
                    request.data["CustomerIsInAccounting"] = False

        return super(SalesViewSet, self).initial(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if request.user.groups.filter(name='foroosh').count() == 0:
            return Response({})

        result = super(SalesViewSet, self).list(request, *args, **kwargs)
        for d in result.data["results"]:
            positionDoc = PositionsDocument.objects.filter(
                positionID=d["positionID"],
                companyID=request.user.current_company_id,
            )

            d["commentCount"] = SaleConversationComments.objects.filter(saleConversationLink=d["id"]).count()
            items = SaleConversationItems.objects.filter(saleConversationLink=d["id"])
            d["productCount"] = items.count()
            totalSum = 0
            for i in items:
                sum = (i.amount * i.fee) - i.off
                totalSum += sum
            d["total"] = totalSum

            if positionDoc.count() != 0:
                positionDoc = positionDoc[0]
                profileInstance = Profile.objects.get(userID=positionDoc.userID)
                d["positionName"] = positionDoc.profileName
                d["positionSemat"] = positionDoc.chartName
                d["avatar"] = profileInstance.extra["profileAvatar"]["url"]
            else:
                d["positionName"] = "حذف شده"
                d["positionSemat"] = "حذف شده"
                d["avatar"] = "/static/images/avatar_empty.jpg"

        return result

    def template_view(self, request):
        return render_to_response('Sales/base.html', {}, context_instance=RequestContext(request))

    def template_view_SalesProfilePhones(self, request):
        return render_to_response('Sales/Profile/justPhones.html', {}, context_instance=RequestContext(request))

    def template_view_Karshenasi(self, request):
        return render_to_response('Sales/Tamin/Karshenasi/base.html', {}, context_instance=RequestContext(request))

    def template_view_sales_conversations(self, request):
        return render_to_response('Sales/Conversations/base.html', {}, context_instance=RequestContext(request))

    def template_view_SalesProfile(self, request):
        return render_to_response('Sales/Profile/base.html', {}, context_instance=RequestContext(request))

    def template_view_saleConv(self, request):
        return render_to_response('Sales/Conversations/conversation.html', {}, context_instance=RequestContext(request))

    def template_view_sales_tataabogh(self, request):
        return render_to_response('Sales/Tataabogh/base.html', {}, context_instance=RequestContext(request))

    def template_view_saleaddbasket(self, request):
        return render_to_response('Sales/Basket/add.html', {}, context_instance=RequestContext(request))

    def template_view_SendSMS(self, request):
        return render_to_response('Sales/SMS/base.html', {}, context_instance=RequestContext(request))

    def template_view_sales_conversations_add_new(self, request):
        return render_to_response('Sales/Conversations/add.html', {}, context_instance=RequestContext(request))

    def template_view_salesMojoodi(self, request):
        return render_to_response('Sales/Mojoodi/base.html', {}, context_instance=RequestContext(request))

    def template_view_sales_customer_profile_modal(self, request):
        return render_to_response('Sales/Profile/add.html', {}, context_instance=RequestContext(request))



    def template_view_HavalehForoosh(self, request):
        return render_to_response('Sales/HavalehForoosh/base.html', {}, context_instance=RequestContext(request))

    def template_view_HavalehForooshChange(self, request):
        return render_to_response('Sales/HavalehForoosh/HavalehForooshChange.html', {},
                                  context_instance=RequestContext(request))

    def template_view_HavalehForooshDetails(self, request):
        return render_to_response('Sales/HavalehForoosh/details_base.html', {},
                                  context_instance=RequestContext(request))


    def template_view_OldHavalehForoosh(self, request):
        return render_to_response('Sales/HavalehForooshOld/base.html', {}, context_instance=RequestContext(request))

    def template_view_OldHavalehForooshChange(self, request):
        return render_to_response('Sales/HavalehForooshOld/HavalehForooshChange.html', {},
                                  context_instance=RequestContext(request))

    def template_view_OldHavalehForooshDetails(self, request):
        return render_to_response('Sales/HavalehForooshOld/details_base.html', {},
                                  context_instance=RequestContext(request))


    def template_view_MojoodiGhabeleForooshpartial_aniling(self, request):
        return render_to_response('Sales/Mojoodi/partial_aniling.html', {},
                                  context_instance=RequestContext(request))

    def template_view_MojoodiGhabeleForooshpartial_nokteh_keifi(self, request):
        return render_to_response('Sales/Mojoodi/partial_nokteh_keifi.html', {},
                                  context_instance=RequestContext(request))

    def template_view_MojoodiGhabeleForooshpartial_sefaresh(self, request):
        return render_to_response('Sales/Mojoodi/partial_sefaresh.html', {},
                                  context_instance=RequestContext(request))

    def template_view_MojoodiGhabeleForooshpartial_setare_dar(self, request):
        return render_to_response('Sales/Mojoodi/partial_setare_dar.html', {},
                                  context_instance=RequestContext(request))

    def template_view_MojoodiGhabeleForooshpartial_tozihat(self, request):
        return render_to_response('Sales/Mojoodi/partial_tozihat.html', {},
                                  context_instance=RequestContext(request))


    def template_view_sales_report_trace_havaleh_foroosh(self, request):
        return render_to_response('Sales/reports/havalehFforoosh/report_trace_havaleh_foroosh.html', {},
                                  context_instance=RequestContext(request))



    def template_view_SalesProfileDetails(self, request):
        SaleCustomerFormDetailsFormValidation = SaleCustomerFormDetailsFormV()
        return render_to_response('Sales/Profile/Details/base.html', {
            "SaleCustomerFormDetailsFormValidation": SaleCustomerFormDetailsFormValidation
        }, context_instance=RequestContext(request))

    def template_view_sales_conversations_items(self, request):
        return render_to_response('Sales/Conversations/items/base.html', {},
                                  context_instance=RequestContext(request))

    def template_view_Khoroj(self, request):
        return render_to_response('Sales/Khorooj/base.html', {},
                                  context_instance=RequestContext(request))

    def template_view_MojoodiGhabeleForooshBase(self, request):
        current_year = getCurrentYearShamsi()
        return render_to_response('Sales/Mojoodi/base.html', {'current_year':current_year},
                                  context_instance=RequestContext(request))

    def template_view_Khoroj_Details(self, request):
        return render_to_response('Sales/Khorooj/details.html', {},
                                  context_instance=RequestContext(request))

    def template_view_KhoroojRep1(self, request):
        return render_to_response('Sales/reports/khorooj/report1.html', {},
                                  context_instance=RequestContext(request))

    def template_view_Old_Khoroj(self, request):
        return render_to_response('Sales/KhoroojOld/base.html', {},
                                  context_instance=RequestContext(request))

    def template_view_Old_Khoroj_Details(self, request):
        return render_to_response('Sales/KhoroojOld/details.html', {},
                                  context_instance=RequestContext(request))


    def template_view_KarshenasiTahili(self, request):
        return render_to_response('Sales/Tamin/Karshenasi/tahlil.html', {},
                                  context_instance=RequestContext(request))

    def template_view_SalesCustomerTahili(self, request):
        return render_to_response('Sales/Tamin/Karshenasi/customerTahlil.html', {},
                                  context_instance=RequestContext(request))

    def template_view_SalesCustomerTahiliDetails(self, request):
        return render_to_response('Sales/Tamin/Karshenasi/customerTahlilDetails.html', {},
                                  context_instance=RequestContext(request))

    def template_view_salesKarshenasiAddNew_modal(self, request):
        return render_to_response('Sales/Tamin/Karshenasi/addedit.html', {},
                                  context_instance=RequestContext(request))

    def template_view_showSignBodyPrc(self, request):
        return render_to_response('Sales/sign/signBody.html', {},
                                  context_instance=RequestContext(request))

    def template_view_sales_report_base(self, request):
        return render_to_response('Sales/reports/base.html', {},
                                  context_instance=RequestContext(request))

    def getCustomers(self):
        customers = cache.get("****Customers")
        if not customers:

            pool = ConnectionPools.objects.get(name="vwSLECstmrs")
            sql = pool.sqls[0]["code"]
            connection = Connections.objects.get(databaseName="sgdb")
            connection = ConnectionsViewSet().getConnection(connection)
            connection.execute(sql)
            sql_res = connection.fetchall()
            rows = []
            for row in sql_res:
                ccc = row
                ccc['CustomerID'] = row['CstmrCode']
                ccc['CustomerName'] = row['CstmrName'].replace('ي', 'ی').replace('ش', 'ش').replace('ک', 'ک')
                rows.append(ccc)
            cache.set("****Customers", rows, 60)

        return cache.get("****Customers")

    @list_route(methods=["GET"])
    def getCustomerNames(self, request):
        customers = cache.get("****Customers")
        # customers = None
        if not customers:

            pool = ConnectionPools.objects.get(name="vwSLECstmrs")
            sql = pool.sqls[0]["code"]
            connection = Connections.objects.get(databaseName="sgdb")
            connection = ConnectionsViewSet().getConnection(connection)
            connection.execute(sql)
            sql_res = connection.fetchall()
            sql_res = convert_sqlresultstr_to_valid_str(sql_res)
            rows = []
            for row in sql_res:
                rows.append({"CustomerID": row['CstmrCode'],
                             "CustomerName": row['CstmrName']})
            cache.set("****Customers", rows, 60)
            customers = rows

        searchText = request.query_params['searchText']

        customers = query(customers).where(
            lambda x: ((searchText in x["CustomerName"]) or (searchText in str(x["CustomerID"])))).take(
            60).to_list()
        return Response(customers)

    sqlserverIP = "172.16.5.10"
    sqlserverUsername = "rahsoon"
    sqlserverPassword = "****"
    sqlserverDBName = "sgdb"

    def hamkaran_GetFactorsGroupByKala(self, hamkaranCustomerCode):
        conn = pymssql.connect(self.sqlserverIP, self.sqlserverUsername, self.sqlserverPassword,
                               self.sqlserverDBName, charset="UTF-8", as_dict=True)
        cursor = conn.cursor()
        sql = """
              SELECT TOP 9000
                max(vsf.PartName) as [partName],
                PartCode,verfCode
                       SUBSTRING(vsf.PartCode, 1, 2) as [sharh],
                       SUBSTRING(vsf.PartCode, 3, 1) as [BP],
                       SUBSTRING(vsf.PartCode, 4, 1) as [TEMPER],
                       SUBSTRING(vsf.PartCode, 5, 1) as [sath],
                       SUBSTRING(vsf.PartCode, 6, 2) as [zekhamat],
                       SUBSTRING(vsf.PartCode, 8, 3) as [arz],
                       SUBSTRING(vsf.PartCode, 11, 1) as [darajeh],
                       SUBSTRING(vsf.PartCode, 12, 3) as [tool],
                       sum(vsf.Qty) as [sumQty]
                  from
                  [sgdb].[sle].[vwSLERepFactor]  vsf

                   where VchDate between '2012-03-21' and '2022-03-21'
                  and vsf.CstmrRef = %s

                  group by vsf.PartCode
                  order by sum(vsf.Qty) desc
            """ % (hamkaranCustomerCode,)
        cursor.execute(sql)
        return cursor.fetchall()

    def hamkaran_GetMojoodi(self, strStartDate='2019-03-21', strEndDate='2020-03-21'):
        sql = """
                    SELECT
                    (select top 1 sss.PartCode  FROM [sgdb].[inv].[Part] sss where sss.Serial = ttt.PartRef) as [PartCode],
                    (select top 1 sss.PartName  FROM [sgdb].[inv].[Part] sss where sss.Serial = ttt.PartRef) as [PartName],
                    '13'+ REPLACE(gnr.sgfn_DateToShamsiDate(max(ttt.XDate)), '/','/')  as latestDate,
                    ttt.PartRef,
                    sum(ttt.XQtyRatio) as sumOf,
                    (select isnull(sum(dee.Qty),0) from [sgdb].[sle].[vwSLEPreFactItm] dee where dee.PartRef = ttt.PartRef and dee.Status = 0) as sumPish
                    ,
                    (select isnull(sum(dee.Qty),0) from [sgdb].[sle].[vwSLEPreFactItm] dee where dee.PartRef = ttt.PartRef and dee.Status = 1) as sumPishOK
                      FROM [sgdb].[inv].[vwCardex] ttt
                      where
                     SUBSTRING((
                            select top 1 sss.PartCode
                            FROM [sgdb].[inv].[Part] sss
                            where
                            sss.Serial = ttt.PartRef), 1, 2) in ('66','77','88')
                            and  SUBSTRING((
                            select top 1 sss.PartCode
                            FROM [sgdb].[inv].[Part] sss
                            where
                            sss.Serial = ttt.PartRef), 5, 6) not in('000000')
                        and VchDate between '%s' and '%s'
                      group by (ttt.PartRef)
                      having sum(ttt.XQtyRatio) > 0
                      order by sum(ttt.XQtyRatio) desc
            """ % (strStartDate, strEndDate,)

        conn = pymssql.connect(self.sqlserverIP, self.sqlserverUsername, self.sqlserverPassword,
                               self.sqlserverDBName, charset="UTF-8", as_dict=True)
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def hamkaran_GetCardex(self, strStartDate='2019-03-21', strEndDate='2020-03-21'):
        sql = """
                select
                CASE
                when (SUBSTRING(prt.PartCode, 1, 2) in ('66') and SUBSTRING(prt.PartCode, 3, 1) in ('7'))
                then stuff(prt.PartCode,8,3, cast(cast(SUBSTRING(prt.PartCode, 8, 3) as INT)-%d as NVARCHAR(3) )) else prt.PartCode end as [PartCode],
                prt.PartName,
                vsf.VchItmId,
                vsf.XQtyRatio,
                vsf.XDate,
                vsf.Date
                from
                  [sgdb].[inv].[vwCardex]  vsf
                  inner join [sgdb].[inv].[Part] prt on vsf.PartRef = prt.Serial

                  where
                  SUBSTRING(prt.PartCode, 1, 2) in ('66','77','88')
                  and
                  SUBSTRING(prt.PartCode, 5, 6) not in('000000')
                  and
                  VchDate between '%s' and '%s'

            """ % (self.trim, strStartDate, strEndDate,)

        conn = pymssql.connect(self.sqlserverIP, self.sqlserverUsername, self.sqlserverPassword,
                               self.sqlserverDBName, charset="UTF-8", as_dict=True)
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def hamkaran_GetCardexAllColumns(self, strStartDate='2019-03-21', strEndDate='2020-03-21'):
        sql = """
                select
                CASE
                when (SUBSTRING(prt.PartCode, 1, 2) in ('66') and SUBSTRING(prt.PartCode, 3, 1) in ('7'))
                then stuff(prt.PartCode,8,3, cast(cast(SUBSTRING(prt.PartCode, 8, 3) as INT)-%d as NVARCHAR(3) )) else prt.PartCode end as [PartCode],
                prt.PartName,
                vsf.*
                from
                  [sgdb].[inv].[vwCardex2 ]  vsf
                  inner join [sgdb].[inv].[Part] prt on vsf.PartRef = prt.Serial

                  where
                  SUBSTRING(prt.PartCode, 1, 2) in ('66','77','88')
                  and
                  SUBSTRING(prt.PartCode, 5, 6) not in('000000')
                  and
                  VchDate between '%s' and '%s'

            """ % (self.trim, strStartDate, strEndDate,)

        conn = pymssql.connect(self.sqlserverIP, self.sqlserverUsername, self.sqlserverPassword,
                               self.sqlserverDBName, charset="UTF-8", as_dict=True)
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def pollCurrentCardex(self):
        sql = """

        """

    def hamkaran_GetOpenPish(self):
        sql = """
                select
                www.PartCode,
                www.PartName,
                www.VchItmId,
                www.PartRef,
                www.Status,
                www.Qty,
                www.CstmrCode,
                www.VchHdrRef,
                www.VchNo

                from [sgdb].[sle].[vwSLERepPreFact] www

                where

                www.HStatus in (0,1) and SUBSTRING(www.PartCode, 1, 2) in ('66','77','88')

            """

        conn = pymssql.connect(self.sqlserverIP, self.sqlserverUsername, self.sqlserverPassword,
                               self.sqlserverDBName, charset="UTF-8", as_dict=True)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        # getting ignorance pish
        igones = list(PishfactorsIgnore.objects.filter())

        for r in result:
            r['isAccountable'] = True
            for i in igones:
                if (r['CstmrCode'] == i.CstmrCode) and \
                        (r['VchItmId'] == i.VchItmId) and \
                        (r['VchHdrRef'] == i.VchHdrRef) and \
                        (r['PartRef'] == i.PartRef) and \
                        (r['VchNo'] == i.VchNo):
                    r['isAccountable'] = False

        return result



    @list_route(methods=["POST"])
    def send_free_sms(self, request, *args, **kwargs):
        if request.user.groups.filter(
                Q(name__contains="foroosh") |
                Q(name__contains="group_namayendgi_8_ostan") |
                Q(name__contains="ext")
        ).count() == 0:
            raise Exception("مجوز دسترسی ندارید")

        sendSMS(request.data["number"], request.data["body"])
        return Response({})

    @list_route(methods=["POST"])
    def send_free_sms_async(self, request, *args, **kwargs):
        if request.user.groups.filter(
                Q(name__contains="foroosh") |
                Q(name__contains="group_namayendgi_8_ostan") |
                Q(name__contains="ext")
        ).count() == 0:
            raise Exception("مجوز دسترسی ندارید")

        sendSMS.delay(request.data["number"], request.data["body"])
        return Response({})


    @detail_route(methods=["GET"])
    def getTataboghByCustomer(self, request, *args, **kwargs):
        customerProfileInstance = SalesCustomerProfile.objects.get(id=kwargs["id"])
        factors = self.hamkaran_GetFactorsGroupByKala(customerProfileInstance.hamkaranCode)

        # getting current mojoodi
        # it contains all details about mojoodi
        mojoodiList = cache.get('currentCardexGroup_' + str(request.user.id))
        if not mojoodiList:
            self.getInCache(request)
            mojoodiList = cache.get('currentCardexGroup_' + str(request.user.id))

        # getting future from google spreadsheet
        futureMylist = cache.get("future_" + str(request.user.id))
        if not futureMylist:
            self.getInCache(request)
            futureMylist = cache.get("future_" + str(request.user.id))

        # this line skip first row
        futureMylist = futureMylist[1::]
        # converting CSV ro raw list
        for m in futureMylist:
            for i in range(0, 10):
                m[i] = int(m[i].replace(",", "")) if m[i].replace(",", "").isdigit() else m[i]

        # joining map list
        tataaboghBy = request.query_params["f"].split("_")

        def convBool(b):
            if b == "true":
                return True
            else:
                return False

        tataaboghBy = list(map(convBool, tataaboghBy))

        # convs = SaleConversations.objects.filter(Open=True, PrefactorID__exists=False)
        # convItems = SaleConversationItems.objects.filter(
        #     saleConversationLink__in=[str(c.id) for c in convs])
        # convItems = SaleConversationItemsSerializer(instance=convItems, many=True).data

        # for c in convItems:
        #     ff = self.convertCodeToSep(c["itemID"])
        #     c.update(ff)

        for f in factors:
            mq = query(mojoodiList)
            if tataaboghBy[0]:
                mq = mq.where(lambda x: int(x['temper']) == int(f["TEMPER"]))
            if tataaboghBy[1]:
                mq = mq.where(lambda x: x['sath'] == "Stone" if f["sath"] == "2" else "Bright")
            if tataaboghBy[2]:
                mq = mq.where(lambda x: int(x['zekhamat']) == int(f["zekhamat"]))
            if tataaboghBy[3]:
                mq = mq.where(lambda x: int(x['arz']) == int(f["arz"]))
            if tataaboghBy[4]:
                mq = mq.where(lambda x: int(x['tool']) == int(f["tool"]))

            # conv
            # mc = query(convItems)
            # if tataaboghBy[0]:
            #     mc = mc.where(lambda x: int(x['temper']) == int(f["TEMPER"]))
            # if tataaboghBy[1]:
            #     mc = mc.where(lambda x: x['sath'] == "Stone" if f["sath"] == "2" else "Bright")
            # if tataaboghBy[2]:
            #     mc = mc.where(lambda x: int(x['zekhamat']) == int(f["zekhamat"]))
            # if tataaboghBy[3]:
            #     mc = mc.where(lambda x: int(x['arz']) == int(f["arz"]))
            # if tataaboghBy[4]:
            #     mc = mc.where(lambda x: int(x['tool']) == int(f["tool"]))

            # f["mojoodi"] = mq.sum(lambda x: x['total']) - (
            #     mq.sum(lambda x: x['sumOfPish']) + mq.sum(lambda x: x['sumOfPishOK'])) - mc.sum(lambda x: x['amount'])
            f["mojoodi"] = mq.sum(lambda x: x['total'])
            # getting conv count

            fq = query(futureMylist)
            fq = fq.where(lambda x: x[1] == int(f["TEMPER"]))
            fq = fq.where(lambda x: x[2] == "Stone" if f["sath"] == "2" else "Bright")
            fq = fq.where(lambda x: x[3] == int(f["zekhamat"]))
            fq = fq.where(lambda x: x[5] == int(f["arz"]))
            fq = fq.where(lambda x: x[6] == int(f["tool"]))

            f["future"] = fq.sum(lambda x: x[8])

        return Response({'factors': factors})
