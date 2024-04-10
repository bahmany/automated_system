from django.shortcuts import render_to_response
from django.template import RequestContext
from amspApp.Infrustructures.odoo_connector.connectors import OdooConnector
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amsp import settings
from amsp.settings import  PASSWORD_DBNAME, PASSWORD_USERNAME, PASSWORD_PASS
from amspApp.CompaniesManagment.Connections.models import ConnectionPools, Connections
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsViews import ConnectionsViewSet
from amspApp.Trace.models import TraceTypes, TraceEntry
from amspApp.Trace.serializers.TraceSerializers import TraceTypesSerializer, TraceEntrySerializer
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class TraceEntryViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = TraceEntry.objects.all().order_by("-id")
    serializer_class = TraceEntrySerializer
    pagination_class = DetailsPagination
    pagination_class.page_size = 100

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = posiIns.positionID
        return super(TraceEntryViewSet, self).initial(request, *args, **kwargs)

    @list_route(methods=["get"])
    def get_user_activities(self, request, *args, **kwargs):
        positionInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        typesInstance = TraceTypes.objects.filter(permittedUsers__positionID=positionInstance.positionID).order_by(
            "name")
        tps = TraceTypesSerializer(instance=typesInstance, many=True).data

        return Response(tps)

    @detail_route(methods=["get"])
    def get_cardex_vch(self, request, *args, **kwargs):
        if not kwargs["id"].isdigit():
            return Response({})
        stockID = request.query_params.get("stock")
        pool = ConnectionPools.objects.get(name="AccViewCardex")
        sql = pool.sqls[0]["code"]
        sql = sql.replace("<:int_vchNum:>", kwargs['id'])
        sql = sql.replace("<:int_stock:>", stockID)
        connection = Connections.objects.get(databaseName="sgdb")
        connection = ConnectionsViewSet().getConnection(connection)
        connection.execute(sql)
        sql_res = connection.fetchall()
        return Response({
            "id": 1,
            "res": sql_res
        })

    @detail_route(methods=["get"])
    def get_odoo_inventory_details(self, request, *args, **kwargs):
        odoo = OdooConnector(endpoint=settings.ODOO_HTTP_REFERER,
                             dbname=PASSWORD_DBNAME,
                             username=PASSWORD_USERNAME,
                             password=PASSWORD_PASS)
        # odoo = OdooConnector(endpoint=ODOO_Platform,
        #                      dbname='odoodb',
        #                      username='bahmanymb@gmail.com',
        #                      password='****')
        uid = odoo.connect()
        # searching for user
        stock_picking = odoo.search(uid=uid,
                             model='stock.picking',
                             action='search_read',
                             queries=[[['name', '=', "WH/IN/" + kwargs.get("id")]]])

        purchase = odoo.search(uid=uid,
                             model='purchase.order',
                             action='search_read',
                             queries=[[['id', '=',stock_picking[0]["purchase_id"][0] ]]])

        purchase_line = odoo.search(uid=uid,
                             model='purchase.order.line',
                             action='search_read',
                             queries=[[['order_id', '=',purchase[0]["id"] ]]])

        return Response({
            "stock":stock_picking[0],
            "purchase":purchase[0],
            "purchase_line":purchase_line[0],
        })

    # @list_route(methods=["post"])
    # def updateRow(self, request, *args, **kwargs):
    #     data = request.data
    #     changed = False
    #     self.queryset.delete()
    #     for d in data:
    #         if d.get('sl') and d.get('gl') and d.get('markazeTashim') and d.get('percent'):
    #             ser = self.serializer_class(
    #                 data=d
    #             )
    #             ser.is_valid(raise_exception=True)
    #             ser.save()
    #             changed = True
    # #     return Response({"msg": changed})
    #
    # def list(self, request, *args, **kwargs):
    #     self.serializer_class.Meta.depth = 2
    #
    #     return super(TraceTypesViewSet, self).list(request, *args, **kwargs)
    #
    # @detail_route(methods=["GET"])
    # def ret(self, request, *args, **kwargs):
    #     self.serializer_class.Meta.depth = 1
    #     rrr = self.retrieve(request, *args, **kwargs)
    #     return rrr
    #
    # def retrieve(self, request, *args, **kwargs):
    #     # self.serializer_class.Meta.depth = 1
    #     return super(TraceTypesViewSet, self).retrieve(request, *args, **kwargs)
    #
    def template_view(self, request):
        return render_to_response('Trace/Entry/base.html', {}, context_instance=RequestContext(request))
