from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Connections.models import ConnectionPools, Connections
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsViews import ConnectionsViewSet
from amspApp.Trace.models import TraceCategory
from amspApp.Trace.serializers.TraceSerializers import TraceCategorySerializer
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class TraceCatViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = TraceCategory.objects.all().order_by("-id")
    serializer_class = TraceCategorySerializer
    pagination_class = DetailsPagination
    pagination_class.page_size = 50

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = posiIns.positionID
        return super(TraceCatViewSet, self).initial(request, *args, **kwargs)

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
    #     return Response({"msg": changed})

    def template_view(self, request):
        return render_to_response('Trace/Category/base.html', {}, context_instance=RequestContext(request))


    @list_route(methods=["GET"])
    def get_dest(self, request, *args, **kwargs):
        res = TraceCategory.objects.filter(isItSource = False).order_by("name")
        result = TraceCategorySerializer(instance=res, many=True).data

        return Response(result)

    @list_route(methods=["GET"])
    def get_source(self, request, *args, **kwargs):
        res = TraceCategory.objects.filter(isItSource = True).order_by("name")
        result = TraceCategorySerializer(instance=res, many=True).data

        return Response(result)

    @detail_route(methods=["GET"])
    def getH(self, request, *args, **kwargs):
        pool = ConnectionPools.objects.get(name="AccStock")
        sql = pool.sqls[0]["code"]
        sql = sql.replace("<:int__code:>", kwargs['id'])
        connection = Connections.objects.get(databaseName="sgdb")
        connection = ConnectionsViewSet().getConnection(connection)
        connection.execute(sql)
        sql_res = connection.fetchall()

        dt = {}

        if (len(sql_res) == 0):
            return Response({"msg":"notfound"})

        dt["res"] = sql_res

        return Response(dt["res"])

