from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import views
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.ControlProject.models import CalYearsShare, CalYears
from amspApp.ControlProject.permissions.ControlProjectBase import IsOwnerOrReadOnly_CostCol
from amspApp.ControlProject.serializers.ControlProjectYearsShareSerializer import ControlProjectYearsShareSerializer
from amspApp.Infrustructures.Classes.MongoEngineSearchFilterBackend import MongoSearchFilter, FilterCompanyID
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class ControlProjectYearsShareTemplateView(views.APIView):
    def get(self, request, *args, **kwargs):
        return render_to_response(
            "ControlProject/Years/ShareUsers.html",
            {}, context_instance=RequestContext(request))


class ControlProjectYearsShareViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = ControlProjectYearsShareSerializer
    queryset = CalYearsShare.objects.all().order_by("-id")

    # permission_classes = (IsOwnerOrReadOnly_CostCol,)
    # filter_backends = (MongoSearchFilter)


    def list(self, request, *args, **kwargs):
        result = super(ControlProjectYearsShareViewSet, self).list(request, *args, **kwargs)
        for r in result.data:
            positionInstance = PositionsDocument.objects.filter(positionID = r["positionID"])
            if positionInstance.count != 0:
                positionInstance = positionInstance[0]
                r["avatar"] = positionInstance.avatar
                r["profileName"] = positionInstance.profileName
                r["chartName"] = positionInstance.chartName
                r["canEdit"] = bool(r["perType"])
        return result


    def get_queryset(self):
        self.queryset = self.queryset.filter(calYearID = self.kwargs["Year_id"])
        return super(ControlProjectYearsShareViewSet, self).get_queryset()


    def create(self, request, *args, **kwargs):
        self.queryset.filter(calYearID=kwargs["Year_id"]).delete()
        positionIds = []
        yearInstance = CalYears.objects.get(id=kwargs["Year_id"])
        currentPositionID = GetPositionViewset().GetCurrentPositionDocumentInstance(request).positionID
        for item in request.data:
            userShare = {
                "calYearID": yearInstance,
                "postPositionID": currentPositionID,
                "positionID": item["positionID"],
                "perType": int(item["canEdit"]) if "canEdit" in item else 0
            }
            serial = self.serializer_class(data=userShare)
            serial.is_valid(raise_exception=True)
            serial.save()
        return Response({})
