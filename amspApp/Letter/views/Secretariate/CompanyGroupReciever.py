from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework_mongoengine import viewsets
from amspApp.CompaniesManagment.Positions.models import Position
from amspApp.Infrustructures.Classes.PublicFilters import QuerySetFilter
from amspApp.Letter.models import CompanyRecieverGroup
from amspApp.Letter.serializers.LetterSecretariatSerializer import CompanyRecieverGroupSerializer
from amspApp._Share.ListPagination import DetailsPagination


class CompanyGroupsRecieverViewSet(viewsets.ModelViewSet):
    pagination_class = DetailsPagination
    lookup_field = "id"
    serializer_class = CompanyRecieverGroupSerializer

    def template_view_company_group(self, request, *args, **kwargs):
        return render_to_response("letter/Secretariat/CompanyGroups/base.html",
            {}, context_instance=RequestContext(request))

    def get_queryset(self):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)

        if 'q' in self.request.query_params.keys():
            if self.request.query_params["q"] != "":
                if self.request.query_params["q"] != "undefined":
                    return  CompanyRecieverGroup.objects.filter(companyID=self.request.user.current_company.id,
                                                                        name__contains=self.request.query_params["q"])

        return CompanyRecieverGroup.objects.filter(companyID=self.request.user.current_company.id)

    def create(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        request.data["postPositionID"] = pos.id
        request.data["companyID"] = self.request.user.current_company.id
        return super(CompanyGroupsRecieverViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        request.data["postPositionID"] = pos.id
        request.data["companyID"] = self.request.user.current_company.id
        return super(CompanyGroupsRecieverViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)

        return super(CompanyGroupsRecieverViewSet, self).destroy(request, *args, **kwargs)
