from django.shortcuts import render_to_response
from django.template import RequestContext
from mongoengine import Q
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.BI.DataTables.models import DataTable
from amspApp.BI.DataTables.serializers.DataTableSerializer import DataTableSerializer
from amspApp._Share.ListPagination import DetailsPagination, AllListPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class DataTableViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = DataTable.objects.all().order_by("-id")
    serializer_class = DataTableSerializer
    pagination_class = DetailsPagination
    pagination_class.page_size = 250
    pagination_class.max_page_size = 250
    def get_queryset(self):
        posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(self.request)

        if "q" in self.request.query_params:
            if self.request.query_params["q"] != "undefined":
                if self.request.query_params["q"] != "":
                    q = self.request.query_params["q"]
                    self.queryset = self.queryset.filter(Q(name__contains=q) | Q(desc__contains=q))

        self.queryset = self.queryset.filter(
            Q(position_id=posInstance.positionID) |
            Q(publishedUsers__list__positionID=posInstance.positionID))
        return super(DataTableViewSet, self).get_queryset()

    def checkItemPermission(self, dictItem, posInstance):

        dictItem["permission"] = 3  # readonly

        if dictItem["position_id"] == posInstance.positionID:
            dictItem["permission"] = 1  # owner
        if dictItem["position_id"] != posInstance.positionID:
            for l in dictItem["publishedUsers"]["list"]:
                if l["positionID"] == posInstance.positionID:
                    if "canEdit" in l:
                        if l["canEdit"] == True:
                            dictItem["permission"] = 2  # canEdit

        if dictItem["permission"] != 1:
            posDoc = GetPositionViewset().GetNecInfoOfPos(
                PositionsDocument.objects.get(positionID=dictItem["position_id"]))
            dictItem["ownerPos"] = posDoc
        return dictItem

    def list(self, request, *args, **kwargs):
        posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(self.request)
        res = super(DataTableViewSet, self).list(request, *args, **kwargs)
        for d in res.data["results"]:
            d = self.checkItemPermission(d, posInstance)
        return res

    @detail_route(methods=["GET"])
    def getWithNoPer(self, request, *args, **kwargs):
        result = DataTable.objects.get(id = kwargs.get("id"))
        serial = DataTableSerializer(instance=result).data
        return Response(serial)

    @list_route(methods=["GET"])
    def getAllTabls(self, request, *args, **kwargs):
        self.pagination_class = AllListPagination
        res = self.list(request, *args, **kwargs)
        return res

    @detail_route(methods=["GET"])
    def getDataTableCols(self, request, *args, **kwargs):
        dataTableInstance = self.queryset.get(id=kwargs.get("id"))
        return Response({"cols": dataTableInstance.fields['list']})

    def create(self, request, *args, **kwargs):
        posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        companyID = posInstance.companyID
        posID = posInstance.positionID
        request.data['position_id'] = posID
        request.data['companyId'] = companyID
        return super(DataTableViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        ins = self.get_queryset().get(id=kwargs['id'])
        if ins.position_id != posInstance.positionID:
            raise Exception("You not allowed to edit this datatable")
        return super(DataTableViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        ins = self.get_queryset().get(id=kwargs['id'])
        if ins.position_id != posInstance.positionID:
            raise Exception("You not allowed to remove this datatable")
        return super(DataTableViewSet, self).destroy(request, *args, **kwargs)

    def template_view(self, request, *args, **kwargs):
        return render_to_response('DataTables/base.html', {},
                                  context_instance=RequestContext(request))

    def template_view_edit(self, request, *args, **kwargs):
        return render_to_response('DataTables/editDataTable.html', {},
                                  context_instance=RequestContext(request))

    def template_view_share(self, request, *args, **kwargs):
        return render_to_response('DataTables/shareDataTables.html', {},
                                  context_instance=RequestContext(request))

    def template_view_script(self, request, *args, **kwargs):
        return render_to_response('DataTables/scriptDataTables.html', {},
                                  context_instance=RequestContext(request))

    def template_view_value(self, request, *args, **kwargs):
        return render_to_response('DataTables/valueDataTables.html', {},
                                  context_instance=RequestContext(request))
