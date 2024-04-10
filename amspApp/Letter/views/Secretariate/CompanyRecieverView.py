from django.shortcuts import render_to_response
from django.template import RequestContext
from mongoengine import Q
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from amspApp.CompaniesManagment.Positions.models import Position
from amspApp.Infrustructures.Classes.PublicFilters import QuerySetFilter
from amspApp.Letter.models import CompanyRecieverGroup, CompanyReciever
from amspApp.Letter.serializers.LetterSecretariatSerializer import CompanyRecieverGroupSerializer, \
    CompanyRecieverSerializer
from amspApp._Share.ListPagination import DetailsPagination


class CompanyRecieverViewSet(viewsets.ModelViewSet):
    pagination_class = DetailsPagination
    lookup_field = "id"
    serializer_class = CompanyRecieverSerializer

    def template_view_company(self, request, *args, **kwargs):
        return render_to_response("letter/Secretariat/SecCompanies/base.html",
            {}, context_instance=RequestContext(request))

    def get_queryset(self):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        self.queryset = CompanyReciever.objects.all()

        if "q" in self.request.query_params:
            if self.request.query_params["q"] != "":
                if self.request.query_params["q"] != "":
                    self.queryset = self.queryset.filter(
                        Q(name__contains = self.request.query_params["q"]) |
                        Q(groupname__contains = self.request.query_params["q"]))

        return self.queryset

    def list(self, request, *args, **kwargs):
        result = super(CompanyRecieverViewSet, self).list(request, *args, **kwargs)
        return result

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #
    #     return Response(serializer.data)





    def create(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        request.data["postPositionID"] = pos.id
        request.data["companyID"] = self.request.user.current_company.id
        return super(CompanyRecieverViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        request.data["postPositionID"] = pos.id
        request.data["companyID"] = self.request.user.current_company.id
        return super(CompanyRecieverViewSet, self).update(request, *args, **kwargs)
