from datetime import datetime

import pymssql
from rest_framework.decorators import list_route, detail_route
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Connections.models import ConnectionPools, Connections
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsViews import ConnectionsViewSet
from amspApp.Infrustructures.Classes.DateConvertors import sh_to_mil
from amspApp.Infrustructures.Classes.MongoEngineSearchFilterBackend import MongoSearchFilter, FilterCompanyID
from amspApp.Sales.models import SalesCustomerProfile, Exits
from amspApp.Sales.serializers.CustomerProfileSerializer import CustomerProfileSerializer
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class CustomerProfileViewSet(viewsets.ModelViewSet):
    pagination_class = DetailsPagination
    lookup_field = "id"
    serializer_class = CustomerProfileSerializer
    queryset = SalesCustomerProfile.objects.all().order_by('-Open').order_by('-id')
    # permission_classes = (IsOwnerOrReadOnly_CostCol,)
    filter_backends = (MongoSearchFilter, FilterCompanyID, OrderingFilter)
    search_fields = ("name", "hamkaranCode", "desc", "exp__contact__cell", "exp__contact__name")

    sqlserverIP = "172.16.5.10"
    sqlserverUsername = "rahsoon"
    sqlserverPassword = "****"
    sqlserverDBName = "sgdb"

    def checkPerm(self, req):
        if req.user.groups.filter(name__contains="foroosh").count() == 0:
            raise Exception("مجوز دسترسی ندارید")

    def initialize_request(self, request, *args, **kwargs):
        self.checkPerm(request)
        return super(CustomerProfileViewSet, self).initialize_request(request, *args, **kwargs)

    @detail_route(methods=["GET"])
    def getCustomerHamkaran(self, request, *args, **kwargs):
        conn = pymssql.connect(self.sqlserverIP, self.sqlserverUsername, self.sqlserverPassword,
                               self.sqlserverDBName, charset="UTF-8", as_dict=True)
        cursor = conn.cursor()

        sql = """
SELECT TOP 6000

       '13'+ REPLACE(gnr.sgfn_DateToShamsiDate(vsf.VchDate), '/','/')  as [dateshamsi]
      ,cast(SubString('13'+ REPLACE(gnr.sgfn_DateToShamsiDate(vsf.VchDate), '/','/'),6,2) as int) as [month]
      ,vsf.*

	  ,ROW_NUMBER() OVER (Order by vsf.CstmrName) AS RowNumber,
	   SUBSTRING(vsf.PartCode, 1, 2) as [sharh],
	   SUBSTRING(vsf.PartCode, 3, 1) as [BP],
	   SUBSTRING(vsf.PartCode, 4, 1) as [TEMPER],
	   SUBSTRING(vsf.PartCode, 5, 1) as [sath],
	   SUBSTRING(vsf.PartCode, 6, 2) as [zekhamat],
       SUBSTRING(vsf.PartCode, 8, 3) as [arz],
	   SUBSTRING(vsf.PartCode, 11, 1) as [darajeh],
	   SUBSTRING(vsf.PartCode, 12, 3) as [tool]
  FROM
  [sgdb].[sle].[vwSLERepFactor]  vsf

   where VchDate between '2012-03-21' and '2019-03-21'
  and CstmrCode = %s


  order by vsf.VchDate desc
        """ % (kwargs['id'],)

        cursor.execute(sql)
        result_detail = cursor.fetchall()

        cursor = conn.cursor()
        sql = """
                        SELECT TOP 6000
                        Year,
                        count(vsf.Qty) as [tedad],
                        sum(vsf.Qty) as [km],
                        sum(vsf.FactorTotalPrice) as [price],
                        avg(vsf.FactorTotalPrice/vsf.Qty) as [avgprice]

                          FROM
                          [sgdb].[sle].[vwSLERepFactor]  vsf

                           where VchDate between '2012-03-21' and '2020-03-21'
                            and CstmrCode = %s
                          group by vsf.Year
                """ % (kwargs['id'],)

        cursor.execute(sql)
        total_result = cursor.fetchall()

        result = {
            "detail": result_detail,
            "total": total_result,
        }

        return Response(result)

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = posiIns.positionID
            request.data["companyID"] = posiIns.companyID

        return super(CustomerProfileViewSet, self).initial(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if request.user.groups.filter(name='foroosh').count() == 0:
            return Response({})

        result = super(CustomerProfileViewSet, self).list(request, *args, **kwargs)

        return result

    @list_route(methods=["GET"])
    def listMobs(self, request, *args, **kwargs):
        result = super(CustomerProfileViewSet, self).list(request, *args, **kwargs)
        return result

    def convertDLtoCustomer(self, DLRef):
        pool = ConnectionPools.objects.get(name="AccDLToCustomer")
        sql = pool.sqls[0]["code"]
        sql = sql.replace("<:int__lessthan:>", DLRef)
        connection = Connections.objects.get(databaseName="sgdb")
        connection = ConnectionsViewSet().getConnection(connection)
        connection.execute(sql)
        sql_res = connection.fetchall()
        return sql_res

    @list_route(methods=["POST"])
    def saveJustPhone(self, request, *args, **kwargs):
        exitInstance = Exits.objects.get(id=request.data["id"])
        customerCode = self.convertDLtoCustomer(exitInstance.item['DLRef'])[0]['CstmrCode']
        CustomerInstance = SalesCustomerProfile.objects.filter(hamkaranCode=str(customerCode)).first()
        c = {}
        c = CustomerInstance.exp
        if c.get("contact") == None:
            c["contact"] = {}
        if c.get("contact").get("cell") == None:
            c["contact"]["cell"] = ""
        c["contact"]["cell"] = request.data["exp"]["contact"]["cell"]
        c["contact"]["name"] = request.data["exp"]["contact"]["name"]
        ser = CustomerProfileSerializer(instance=CustomerInstance, data={"exp": c})
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({"result": "updated"})

    @detail_route(methods=["GET"])
    def tahlilAccCus(self, request, *args, **kwargs):
        startYear = request.query_params.get('s')
        yearEnd = request.query_params.get('e')
        startDate = datetime.strptime(sh_to_mil("13" + startYear + "/01/01"), "%Y/%m/%d")
        EndDate = datetime.strptime(sh_to_mil("13" + yearEnd + "/12/29"), "%Y/%m/%d")

        startDate = startDate.strftime('%Y/%m/%d')
        EndDate = EndDate.strftime('%Y/%m/%d')

        pool = ConnectionPools.objects.get(name="AccCustomerFinancialHistory")
        sql = pool.sqls[0]["code"]
        sql = sql.replace("<:int__accnumber:>", kwargs['id'])
        sql = sql.replace("<:int__start:>", startYear)
        sql = sql.replace("<:int__end:>", yearEnd)
        sql = sql.replace("<:date__startDate:>", startDate)
        sql = sql.replace("<:date__endDate:>", EndDate)
        connection = Connections.objects.get(databaseName="sgdb")
        connection = ConnectionsViewSet().getConnection(connection)
        connection.execute(sql)
        sql_res = connection.fetchall()

        dt = {}

        dt["AccSathe4"] = sql_res

        sathe5 = []
        pool = ConnectionPools.objects.get(name="AccCustomerFinanceStep5")
        for s in dt["AccSathe4"]:
            sql = pool.sqls[0]["code"]
            sql = sql.replace("<:int__accnumber:>", kwargs['id'])
            sql = sql.replace("<:int__start:>", startYear)
            sql = sql.replace("<:int__end:>", yearEnd)
            sql = sql.replace("<:date__startDate:>", startDate)
            sql = sql.replace("<:date__endDate:>", EndDate)
            sql = sql.replace("<:int__moeen:>", s.get("Code").replace(" ", ""))
            connection = Connections.objects.get(databaseName="sgdb")
            connection = ConnectionsViewSet().getConnection(connection)
            connection.execute(sql)
            s["details"] = connection.fetchall()

        return Response(dt)
