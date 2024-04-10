import pymssql

from asq.initiators import query
from django.core.cache import cache
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.decorators import list_route, detail_route
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.ControlProject.permissions.ControlProjectBase import IsOwnerOrReadOnly_CostCol
from amspApp.Infrustructures.Classes.MongoEngineSearchFilterBackend import MongoSearchFilter, FilterCompanyID
from amspApp.MyProfile.models import Profile
from amspApp.Sales.models import SaleConversations, SaleConversationItems, SaleCurrentBasket
from amspApp.Sales.permissions.basePermissions import CanCruidSale
from amspApp.Sales.serializers.SaleConversationSerializer import SaleConversationSerializer, \
    SaleConversationItemsSerializer, SaleCustomerSaleBasket
from amspApp.Sales.views.SalesView import SalesViewSet
from amspApp._Share.ListPagination import ListPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class SalesConversationItemsViewSet(viewsets.ModelViewSet):
    pagination_class = ListPagination
    pagination_class.page_size = 50
    lookup_field = "id"
    serializer_class = SaleConversationItemsSerializer
    queryset = SaleConversationItems.objects.all().order_by('-id')
    permission_classes = (IsOwnerOrReadOnly_CostCol,)
    filter_backends = (MongoSearchFilter, FilterCompanyID, OrderingFilter)
    search_fields = ("itemName", "comment",)

    sqlserverIP = "172.16.5.10"
    sqlserverUsername = "rahsoon"
    sqlserverPassword = "****"
    sqlserverDBName = "sgdb"

    def checkPerm(self, req):
        if req.user.groups.filter(name__contains="foroosh").count() == 0:
            raise Exception("مجوز دسترسی ندارید")

    def initialize_request(self, request, *args, **kwargs):
        self.checkPerm(request)
        return super(SalesConversationItemsViewSet, self).initialize_request(request, *args, **kwargs)


    def refreshCache(self):
        conn = pymssql.connect(self.sqlserverIP, self.sqlserverUsername, self.sqlserverPassword,
                               self.sqlserverDBName)
        cursor = conn.cursor()
        cursor.execute("""
                                SELECT [Serial]

                                      ,[PartCode]
                                      ,[PartName]
                                      ,[LatinName]
                                      ,[PartNo]
                                        ,SUBSTRING(PartCode, 1, 2) as [sharh],
                                        SUBSTRING(PartCode, 3, 1) as [BP],
                                        SUBSTRING(PartCode, 4, 1) as [TEMPER],
                                        SUBSTRING(PartCode, 5, 1) as [sath],
                                        SUBSTRING(PartCode, 6, 2) as [zekhamat],
                                        SUBSTRING(PartCode, 8, 3) as [arz],
                                        SUBSTRING(PartCode, 11, 1) as [darajeh],
                                        SUBSTRING(PartCode, 12, 3) as [tool]
                                  FROM [sgdb].[inv].[Part]

                                  where SUBSTRING(PartCode, 1, 2) in ('66','77','88','99')
                                  order by serial desc
                    """)
        rows = []
        for row in cursor.fetchall():
            rows.append({"VchItmId": row[0],
                         "PartCode": row[1].replace('ي', 'ی').replace('ش', 'ش').replace('ک', 'ک'),
                         "PartName": row[2].replace('ي', 'ی').replace('ش', 'ش').replace('ک', 'ک'),
                         "MainUnitName": row[3],
                         "sharh": row[4],
                         "BP": row[5],
                         "TEMPER": row[6],
                         "sath": row[7],
                         "zekhamat": row[8],
                         "arz": row[9],
                         "darajeh": row[10],
                         "tool": row[11],
                         }),

        cache.set("****Items", rows, 60)
        return rows

    def get_queryset(self):
        convID = -1
        if "convID" in self.request.query_params:
            self.queryset = self.queryset.filter(saleConversationLink=self.request.query_params["convID"])

        return super(SalesConversationItemsViewSet, self).get_queryset()

    # @list_route(methods=["POST"])
    # def addToBasket(selfrequest, *args, **kwargs):
    #

    def stringCode(self, itemId):
        nm = SalesViewSet().convertCodeToSep(itemId)
        result = " %s -  %s - %s - %s - %s - %s - %s - %s " %(
            nm["noe"],
            nm["keshvar"],
            nm["temper"],
            nm["sath"],
            nm["zekhamat"],
            nm["arz"],
            nm["keifiat"],
            nm["tool"],)
        return result

    @detail_route(methods=["GET"])
    def addFromBasket(self, request, *args, **kwargs):
        # getting all basket
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        baskets = SaleCurrentBasket.objects.all().filter(transfered=False, positionID=posiIns.positionID).order_by('id')
        # baskets = SaleCustomerSaleBasket(baskets, many=True).data
        for b in baskets:
            itt = {}
            itt['positionID'] = posiIns.positionID
            itt['companyID'] = posiIns.companyID
            itt['saleConversationLink'] = kwargs["id"]
            itt['paymentType'] = b.desc["paymentType"]
            itt['itemID'] = b.desc["itemID"]
            itt['itemName'] = b.desc['itemName'] if 'itemName' in b.desc else self.stringCode(b.desc["itemID"])
            itt['amount'] = b.desc["amount"]
            itt['fee'] = b.desc["fee"]
            itt['off'] = b.desc["off"]
            slc = SaleConversationItemsSerializer(data=itt)
            slc.is_valid(raise_exception=True)
            slc.save()
            b.update(transfered=True)
        return Response({})

    @list_route(methods=["GET"])
    def getItemsFromHamkaran(self, request, *args, **kwargs):
        customers = cache.get("****Items")
        if not customers:
            customers = self.refreshCache()

        searchText = ""
        if "search" in request.query_params:
            if request.query_params['search'] != "undefined":
                searchText = request.query_params['search']

        customers = query(customers).where(
            lambda x: ((searchText in x["PartName"]) or (searchText in str(x["PartCode"])))).take(
            60).to_list()
        return Response(customers)

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = posiIns.positionID
            request.data["companyID"] = posiIns.companyID
            request.data["index"] = 0

        return super(SalesConversationItemsViewSet, self).initial(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        result = super(SalesConversationItemsViewSet, self).list(request, *args, **kwargs)
        for d in result.data["results"]:
            positionDoc = PositionsDocument.objects.filter(
                positionID=d["positionID"],
                companyID=request.user.current_company_id,
            )

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
            d["isEditable"] = (d["positionID"] == positionDoc.positionID)

        return result
