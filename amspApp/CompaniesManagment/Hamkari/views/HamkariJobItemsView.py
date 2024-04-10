from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Hamkari.models import HamkariJobs, RequestHamkari
from amspApp.CompaniesManagment.Hamkari.serializers.HamkariSerializer import HamkariJobsSerializer
from amspApp.CompaniesManagment.permissions.CompanyPermissions import CanCruid
from amspApp.Infrustructures.Classes.MongoEngineSearchFilterBackend import MongoSearchFilter, FilterTitle, FilterName
from amspApp._Share.ListPagination import ListPagination, DetailsPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class HamkariJobItemViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = HamkariJobs.objects.all().order_by("-id")
    serializer_class = HamkariJobsSerializer
    pagination_class = DetailsPagination
    filter_backends = (MongoSearchFilter, FilterName)

    permission_name = "Can_Edit_hirings"
    permission_classes = (CanCruid,)


    def get_queryset(self):
        self.queryset = self.queryset.filter(hamkariID = self.kwargs['hamkariID_id'])
        return super(HamkariJobItemViewSet, self).get_queryset()

    def initial(self, request, *args, **kwargs):

        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = posiIns.positionID
            request.data["hamkariID"] = kwargs['hamkariID_id']
        return super(HamkariJobItemViewSet, self).initial(request, *args, **kwargs)


    def list(self, request, *args, **kwargs):

        result = super(HamkariJobItemViewSet, self).list(request, *args, **kwargs)
        for r in result.data["results"]:
            r["registered_count"] = RequestHamkari.objects.filter(jobID = r["id"]).count()
        return result

    # def initialize_request(self, request, *args, **kwargs):
    #
    #     return super(HamkariJobItemViewSet, self).initialize_request(request, *args, **kwargs)



    def create(self, request, *args, **kwargs):
        result = super(HamkariJobItemViewSet, self).create(request, *args, **kwargs)
        return result