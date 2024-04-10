from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework_mongoengine.viewsets import ModelViewSet

from amspApp.BPMSystem.models import SqlTableSelectedItems, ExtraSqlDataForTableSelectedItems
from amspApp.BPMSystem.serializers.SqlTableSelectedItemsSerializer import SqlTableSelectedItemsSerializer, \
    ExtraSqlDataForTableSelectedItemsSerializer
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class SqlTableSelectedItemsViewSet(ModelViewSet):
    lookup_field = 'id'
    queryset = SqlTableSelectedItems.objects.all()
    serializer_class = SqlTableSelectedItemsSerializer
    pagination_class = DetailsPagination

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = str(posiIns.id)
            request.data["companyID"] = posiIns.companyID
        return super(SqlTableSelectedItemsViewSet, self).initial(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        result = super(SqlTableSelectedItemsViewSet, self).create(request, *args, **kwargs)
        result.data["storeData"]["selectedBefore"] = True
        result.data["storeData"]["SqlTableSelectedItemID"] = result.data["id"]
        return result

    def retrieve(self, request, *args, **kwargs):
        result = super(SqlTableSelectedItemsViewSet, self).retrieve(request, *args, **kwargs)
        return result

    @list_route(methods=["post"])
    def addTablePoolExtraValues(self, request, *args, **kwargs):
        # deleting all same key
        ExtraSqlDataForTableSelectedItems.objects.filter(
            sqlTableSelectedItemsLink=request.data.get("SqlTableSelectedItemID")).delete()
        extraDt = dict(
            positionID=str(GetPositionViewset().GetCurrentPositionDocumentInstance(request).id),
            companyID=request.data.get("companyID"),
            sqlTableSelectedItemsLink=request.data.get("SqlTableSelectedItemID"),
            values=request.data.get("extraValues"),
            desc={}, )
        dt = ExtraSqlDataForTableSelectedItemsSerializer(data=extraDt)
        dt.is_valid(raise_exception=True)
        dt.save()
        return Response(dt.data)


