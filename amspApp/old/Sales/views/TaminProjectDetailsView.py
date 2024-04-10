from datetime import datetime

from rest_framework.filters import OrderingFilter
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.ControlProject.permissions.ControlProjectBase import IsOwnerOrReadOnly_CostCol
from amspApp.Infrustructures.Classes.DateConvertors import sh_to_mil, mil_to_sh
from amspApp.Infrustructures.Classes.MongoEngineSearchFilterBackend import MongoSearchFilter, FilterCompanyID
from amspApp.MyProfile.models import Profile
from amspApp.Sales.models import TaminProject, TaminDetails
from amspApp.Sales.permissions.basePermissions import CanCruidSale
from amspApp.Sales.serializers.TaminSerializer import TaminProjectSerializer, TaminDetailsSerializer
from amspApp._Share.ListPagination import ListPagination
from amspApp._Share.ModelViewsPosAndComp import ModelViewMongoPosAndComp
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class TaminProjectDetailsView(ModelViewMongoPosAndComp):

    pagination_class = ListPagination
    lookup_field = "id"
    serializer_class = TaminDetailsSerializer
    queryset = TaminDetails.objects.all().order_by('-id')
    permission_classes = (IsOwnerOrReadOnly_CostCol, CanCruidSale,)
    filter_backends = (MongoSearchFilter, FilterCompanyID, OrderingFilter,)
    search_fields = ("projectName", "factoryName", "desc",)
    convertDateFields = ("tarikheVoroodBeGomrok","tarikheBoresh",)


    def checkPerm(self, req):
        if req.user.groups.filter(name__contains="tamin").count() == 0:
            raise Exception("مجوز دسترسی ندارید")

    def initialize_request(self, request, *args, **kwargs):
        self.checkPerm(request)
        return super(TaminProjectDetailsView, self).initialize_request(request, *args, **kwargs)


    # def initial(self, request, *args, **kwargs):
    #     if request.method != "GET" and request.method != "DELETE":
    #         posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
    #         request.data["positionID"] = posiIns.positionID
    #         request.data["companyID"] = posiIns.companyID
    #         # request.data["projectStartDate"] = datetime.strptime(sh_to_mil(request.data['projectStartDate']), "%Y/%m/%d")
    #
    #     return super(TaminProjectDetailsView, self).initial(request, *args, **kwargs)

    # def retrieve(self, request, *args, **kwargs):
    #     result =  super(TaminProjectViewSet, self).retrieve(request, *args, **kwargs)
    #     result.data['projectStartDate'] = datetime.strptime(sh_to_mil(result.data['projectStartDate']), "%Y/%m/%d")
    #     return result


