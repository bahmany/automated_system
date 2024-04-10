from rest_framework_mongoengine.viewsets import ModelViewSet

from amspApp.BPMSystem.models import TableSelectedItems
from amspApp.BPMSystem.serializers.TableSelectedItemsSerializer import TableSelectedItemsSerializer
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class TableSelectedItemsViewSet(ModelViewSet):
    lookup_field = 'id'
    queryset = TableSelectedItems.objects.all()
    serializer_class = TableSelectedItemsSerializer
    pagination_class = DetailsPagination

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = str(posiIns.id)
            request.data["companyID"] = posiIns.companyID
        return super(TableSelectedItemsViewSet, self).initial(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        result = super(TableSelectedItemsViewSet, self).create(request, *args, **kwargs)
        result.data["storeData"]["selectedBefore"] = True
        result.data["storeData"]["TableSelectedItemID"] = result.data["id"]
        return result

    def retrieve(self, request, *args, **kwargs):
        result = super(TableSelectedItemsViewSet, self).retrieve(request, *args, **kwargs)
        return result



