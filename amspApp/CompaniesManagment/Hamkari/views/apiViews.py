from datetime import datetime

from amspApp.CompaniesManagment.Hamkari.models import Hamkari, HamkariJobs
from amspApp.CompaniesManagment.Hamkari.serializers.HamkariSerializer import HamkariSerializer, HamkariJobsSerializer
from amspApp.CompaniesManagment.permissions.CompanyPermissions import CanCruid
from amspApp.CompaniesManagment.permissions.PermissionChecker import get_permissions
from amspApp.Infrustructures.Classes.DateConvertors import sh_to_mil
from amspApp.Infrustructures.Classes.MongoEngineSearchFilterBackend import MongoSearchFilter, FilterTitle

__author__ = 'mohammad'

from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework_mongoengine import viewsets
from amspApp._Share.ListPagination import DetailsPagination

__author__ = 'mohammad'


class HamkariViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Hamkari.objects.all()
    filter_backends = (MongoSearchFilter, FilterTitle)
    serializer_class = HamkariSerializer
    pagination_class = DetailsPagination
    permission_name = "Can_Edit_hirings"
    permission_classes = (CanCruid,)

    def get_permissions(self):
        return get_permissions(self, HamkariViewSet)

    def get_queryset(self):
        self.queryset = self.queryset.filter(userID=self.request.user.id)
        return self.queryset

    def create(self, request, *args, **kwargs):
        request.data["userID"] = request.user.id
        request.data["startDate"] = datetime.strptime(sh_to_mil(request.data['startDate']), "%Y/%m/%d")
        request.data["endDate"] = datetime.strptime(sh_to_mil(request.data['endDate']), "%Y/%m/%d")
        return super(HamkariViewSet, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        result = super(HamkariViewSet, self).retrieve(request, *args, **kwargs)
        # getting jobs and add to instance
        jobs = HamkariJobs.objects.filter(hamkariID=kwargs['id'])
        jobs = HamkariJobsSerializer(instance=jobs, many=True).data
        result.data["jobs"] = jobs

        return result

    def template_page(self, request, *args, **kwargs):
        return render_to_response("companyManagement/Hamkari/base.html", {},
                                  context_instance=RequestContext(self.request))

    def template_postJob(self, request, *args, **kwargs):
        return render_to_response("companyManagement/Hamkari/NewEditHamkari.html", {},
                                  context_instance=RequestContext(self.request))

    def template_JobItems(self, request, *args, **kwargs):
        return render_to_response("companyManagement/Hamkari/JobItems/base.html", {},
                                  context_instance=RequestContext(self.request))

    def template_RequestHamkariItems(self, request, *args, **kwargs):
        return render_to_response("companyManagement/Hamkari/registeredPersons/base.html", {},
                                  context_instance=RequestContext(self.request))

    def template_AddEditJobItems(self, request, *args, **kwargs):
        return render_to_response("companyManagement/Hamkari/JobItems/modal_addNewJobItem.html", {},
                                  context_instance=RequestContext(self.request))
