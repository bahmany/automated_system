from datetime import datetime

from rest_framework.filters import OrderingFilter
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.ControlProject.permissions.ControlProjectBase import IsOwnerOrReadOnly_CostCol
from amspApp.Infrustructures.Classes.DateConvertors import sh_to_mil, mil_to_sh
from amspApp.Infrustructures.Classes.MongoEngineSearchFilterBackend import MongoSearchFilter, FilterCompanyID
from amspApp.MyProfile.models import Profile
from amspApp.Sales.models import TaminProject
from amspApp.Sales.permissions.basePermissions import CanCruidSale
from amspApp.Sales.serializers.TaminSerializer import TaminProjectSerializer
from amspApp._Share.ListPagination import ListPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class TaminProjectViewSet(viewsets.ModelViewSet):
    pagination_class = ListPagination
    lookup_field = "id"
    serializer_class = TaminProjectSerializer
    queryset = TaminProject.objects.all().order_by('-Open').order_by('-id')
    permission_classes = (IsOwnerOrReadOnly_CostCol, CanCruidSale)
    filter_backends = (MongoSearchFilter, FilterCompanyID, OrderingFilter)
    search_fields = ("projectName", "factoryName", "desc")
    def checkPerm(self, req):
        if req.user.groups.filter(name__contains="tamin").count() == 0:
            raise Exception("مجوز دسترسی ندارید")

    def initialize_request(self, request, *args, **kwargs):
        self.checkPerm(request)
        return super(TaminProjectViewSet, self).initialize_request(request, *args, **kwargs)


    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = posiIns.positionID
            request.data["companyID"] = posiIns.companyID
            request.data["projectStartDate"] = datetime.strptime(sh_to_mil(request.data['projectStartDate']), "%Y/%m/%d")

        return super(TaminProjectViewSet, self).initial(request, *args, **kwargs)

    # def retrieve(self, request, *args, **kwargs):
    #     result =  super(TaminProjectViewSet, self).retrieve(request, *args, **kwargs)
    #     result.data['projectStartDate'] = datetime.strptime(sh_to_mil(result.data['projectStartDate']), "%Y/%m/%d")
    #     return result


    def list(self, request, *args, **kwargs):
        result = super(TaminProjectViewSet, self).list(request, *args, **kwargs)
        for d in result.data["results"]:
            positionDoc = PositionsDocument.objects.filter(
                positionID=d["positionID"],
                companyID=request.user.current_company_id,
            )
            d['projectStartDate'] = mil_to_sh(d['projectStartDate'])

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
