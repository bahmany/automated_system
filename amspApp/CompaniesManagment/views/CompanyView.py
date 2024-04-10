from django.db.models.query_utils import Q
from django.http.request import QueryDict
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets, permissions
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer
from rest_framework.response import Response
from rest_framework import status
# from amspApp.CompaniesManagment import permissions
from amspApp.CompaniesManagment.models import Company
from amspApp.CompaniesManagment.permissions.CompanyPermissions import CanCruid
from amspApp.CompaniesManagment.serializers.CompanySerializers import CompanySerializer
from amspApp._Share.ListPagination import ListPagination
from amspApp.amspUser.models import MyUser


class CompanyViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    ref_name = 'company'
    ref_namePular = 'companies'
    ref_namePularCap = 'Companies'
    ref_nameCap = 'Company'
    # currentUsername = None
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = ListPagination
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)
    permission_classes = CanCruid


    def get_permissions(self):
        # in this section we have some permissions :
        # 1: default company is not deletable
        # 2: accounts must have at least one company

        # if self.request.method in permissions.SAFE_METHODS:
        #     return (permissions.AllowAny(),)


        return (permissions.IsAuthenticated(), CanCruid())





    def create(self, request, *args, **kwargs):
        data = dict(request.data.iterlists()) if type(request.data) == QueryDict else request.data
        data["owner_user"] = request.user.id
        data["details"] = {}
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            result = serializer.create(serializer.validated_data)
            return Response({
                "name":result.name,
                "id":result.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors
                        , status=status.HTTP_400_BAD_REQUEST)





    def get_queryset(self):
        query = self.request.GET.get('query')
        user = MyUser.objects.get(id = self.request.user.id)
        item_per_page = self.request.GET.get('itemPerPage')

        if item_per_page and not item_per_page == 'undefined':
            self.pagination_class.page_size = item_per_page

        if query and not query == 'undefined':
            search_text = self.request.GET['query']
            queryset = Company.objects.filter(
                Q(name__contains=search_text) &
                Q(owner_user=user))
        else:
            queryset = Company.objects.filter(owner_user=user)
        return queryset


