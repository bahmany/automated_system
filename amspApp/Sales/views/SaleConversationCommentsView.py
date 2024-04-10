from rest_framework.decorators import detail_route, list_route
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.ControlProject.permissions.ControlProjectBase import IsOwnerOrReadOnly_CostCol
from amspApp.Infrustructures.Classes.MongoEngineSearchFilterBackend import MongoSearchFilter, FilterCompanyID
from amspApp.MyProfile.models import Profile
from amspApp.Sales.models import SaleConversationComments, SaleConversationCommentsReplays
from amspApp.Sales.permissions.basePermissions import CanCruidSale
from amspApp.Sales.serializers.SaleConversationSerializer import SaleConversationCommentsSerializer, \
    SaleConversationCommentsReplaysSerializer
from amspApp._Share.ListPagination import ListPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class SalesConversationCommentsViewSet(viewsets.ModelViewSet):
    pagination_class = ListPagination
    lookup_field = "id"
    serializer_class = SaleConversationCommentsSerializer
    queryset = SaleConversationComments.objects.all().order_by('-id')
    permission_classes = (IsOwnerOrReadOnly_CostCol,)
    filter_backends = (MongoSearchFilter, FilterCompanyID, OrderingFilter)
    search_fields = ("comment",)

    def checkPerm(self, req):
        if req.user.groups.filter(name__contains="foroosh").count() == 0:
            raise Exception("مجوز دسترسی ندارید")

    def initialize_request(self, request, *args, **kwargs):
        self.checkPerm(request)
        return super(SalesConversationCommentsViewSet, self).initialize_request(request, *args, **kwargs)


    def get_queryset(self):
        if self.request.method == "GET":
            self.queryset = self.queryset.filter(saleConversationLink=self.request.query_params['convID'])
        return super(SalesConversationCommentsViewSet, self).get_queryset()

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = posiIns.positionID
            request.data["companyID"] = posiIns.companyID

        return super(SalesConversationCommentsViewSet, self).initial(request, *args, **kwargs)

    @detail_route(methods=["POST"])
    def AddToReplay(self, request, *args, **kwargs):
        dt = request.data
        dt["SaleConversationCommentsLink"] = kwargs["id"]
        sc = SaleConversationCommentsReplays(**dt)
        sc.save()
        return Response({})

    @list_route(methods=["GET"])
    def removeReplay(self, request, *args, **kwargs):
        ins = SaleConversationCommentsReplays.objects.get(id=request.query_params["replayID"])
        if (ins.positionID == GetPositionViewset().GetCurrentPositionDocumentInstance(request).positionID):
            ins.delete()
        return Response({})

    @detail_route(methods=["GET"])
    def getReplays(self, request, *args, **kwargs):
        all = SaleConversationCommentsReplays.objects.filter(SaleConversationCommentsLink=kwargs["id"]).order_by('-id')
        replays = []
        for pp in all:
            ps = PositionsDocument.objects.get(positionID=pp.positionID)
            replays.append({
                "isEditable": (pp["positionID"] == ps.positionID),
                "positionName": ps.profileName,
                "dateOfPost": pp.dateOfPost,
                "comment": pp.comment,
                "id": pp.id,
            })
        return Response(replays)

    def list(self, request, *args, **kwargs):
        result = super(SalesConversationCommentsViewSet, self).list(request, *args, **kwargs)
        for d in result.data["results"]:
            positionDoc = PositionsDocument.objects.filter(
                positionID=d["positionID"],
                companyID=request.user.current_company_id,
            )

            sls = SaleConversationCommentsReplays.objects.filter(SaleConversationCommentsLink=d["id"]).order_by("-id")
            replays = []
            for pp in sls:
                replays.append({
                    "positionName": PositionsDocument.objects.get(positionID=pp.positionID).profileName,
                    "dateOfPost": pp.dateOfPost,
                    "comment": pp.comment,
                    "id": pp.id,
                })
            d["replays"] = replays
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
