from datetime import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext

from rest_framework import views
from rest_framework.filters import FilterSet, DjangoFilterBackend, SearchFilter, OrderingFilter
from rest_framework_mongoengine import viewsets
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.ControlProject.models import IncomeTypes
from amspApp.ControlProject.permissions.ControlProjectBase import IsOwnerOrReadOnly_CostCol
from amspApp.ControlProject.serializers.ControlProjectIncomeTypesSerializer import ControlProjectIncomeTypesSerializer
from amspApp.Infrustructures.Classes.MongoEngineSearchFilterBackend import MongoSearchFilter, FilterCompanyID
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class ControlProjectIncomeTypeTemplate(views.APIView):
    def get(self, request, *args, **kwargs):
        return render_to_response(
            "ControlProject/Income/base.html",
            {}, context_instance=RequestContext(request))


class ControlProjectIncomeTypeViewSet(viewsets.ModelViewSet):
    pagination_class = DetailsPagination
    lookup_field = "id"
    serializer_class = ControlProjectIncomeTypesSerializer
    queryset = IncomeTypes.objects.all().order_by("-id")
    permission_classes = (IsOwnerOrReadOnly_CostCol,)
    filter_backends = (MongoSearchFilter, FilterCompanyID, OrderingFilter)
    search_fields = ("name",)
    rrrrrr = ""




    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = posiIns.positionID
            request.data["companyID"] = posiIns.companyID
            request.data["postDate"] = datetime.now()
        return super(ControlProjectIncomeTypeViewSet, self).initial(request, *args, **kwargs)

    def get_queryset(self):
        return super(ControlProjectIncomeTypeViewSet, self).get_queryset()

    def list(self, request, *args, **kwargs):
        result = super(ControlProjectIncomeTypeViewSet, self).list(request, *args, **kwargs)
        for r in result.data["results"]:
            posList = PositionsDocument.objects.filter(positionID=r["positionID"]).order_by("-id")
            name = ""
            if posList.count() > 0:
                name = posList[0].profileName
            r["profileName"] = name

        return result
