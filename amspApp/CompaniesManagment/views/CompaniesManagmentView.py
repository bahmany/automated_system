from django.db.models import Q as msql_Q
from django.http.request import QueryDict
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from amspApp.CompaniesManagment.Charts.models import Chart
from amspApp.CompaniesManagment.CompanyProfile.models import CompanyProfile
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.models import Company
from amspApp.CompaniesManagment.serializers.CompanySerializers import CompanySerializer
from amspApp.MyProfile.models import Profile
from amspApp.Virtual.pageLoader import PageLoaderApi
from amspApp._Share.ListPagination import ListPagination, DetailsPagination
from amspApp.amspUser.models import MyUser
from rest_framework import status
from mongoengine import Q

__author__ = 'mohammad'


class CompaniesManagmentViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    # currentUsername = None
    # queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = DetailsPagination

    # pagination_class = ListPagination
    # renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)
    # permission_classes = CanCruid


    def makePermission(self, userID):
        return (Q(userID=userID) &
                (Q(desc__automation__permission__Can_edit_company_profile=True) |
                 Q(desc__automation__permission__Can_Edit_hirings=True) |
                 Q(desc__automation__permission__Can_edit_connections=True) |
                 Q(desc__automation__permission__Can_edit_productions=True) |
                 Q(desc__automation__permission__Can_edit_secretriats=True) |
                 Q(desc__automation__permission__Can_edit_BPMS=True) |
                 Q(desc__automation__permission__Can_edit_documents=True) |
                 Q(desc__automation__permission__Can_Edit_company_chart=True) |
                 Q(desc__automation__permission__Can_remove_members=True) |
                 Q(desc__automation__permission__Can_edit_peoples_to_hire=True
                   )))

    def makeCompanyCanEditFilter(self, userID):
        positionInstances = PositionsDocument.objects.filter(self.makePermission(userID))
        return msql_Q(owner_user=self.request.user.id) | msql_Q(
            id__in=[x['companyID'] for x in positionInstances]
        )

    def get_queryset(self):
        # this is for permission
        self.queryset = Company.objects.filter(self.makeCompanyCanEditFilter(self.request.user.id)).order_by("-id")
        return self.queryset

    def list(self, request, *args, **kwargs):
        self.get_queryset().order_by("-id")
        self.pagination_class.page_size = 50
        result = super(CompaniesManagmentViewSet, self).list(request, *args, **kwargs)
        companyDocs = CompanyProfile.objects.filter(companyID__in=[x["id"] for x in result.data['results']])
        for d in result.data['results']:
            d["default"] = False
            if d["id"] == request.user.current_company_id:
                d["default"] = True
            currentProfile = companyDocs.get(companyID=d["id"])
            d["logo"] = currentProfile.extra["logo"] if "logo" in currentProfile.extra else ""
            d["brf"] = currentProfile.extra["biefIntroduction"] if "biefIntroduction" in currentProfile.extra else ""
        return result

    @list_route(methods=["get"])
    def getDefault(self, request):
        return Response(self.serializer_class(instance=request.user.current_company).data)

    def create(self, request, *args, **kwargs):
        data = dict(request.data.iterlists()) if type(request.data) == QueryDict else request.data
        data["owner_user"] = request.user.id
        # data["details"] = {}
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            result = serializer.create(serializer.validated_data)
            return Response({
                "name": result.name,
                "id": result.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors
                        , status=status.HTTP_400_BAD_REQUEST)

    def template_page(self, request):
        return render_to_response(
            "companyManagement/CompaniesManagment.html",
            {'currentCompanyName': request.user.current_company.name},
            context_instance=RequestContext(self.request))

    companyMenuMapping = [
        ["Can_Edit_company_chart", "مدیریت چارت ****ی", "chart({'companyid': companyId})","chart"],
        ["Can_edit_company_profile", "پروفایل شرکت", "profile({'companyid': companyId})","profile"],
        ["Can_Edit_hirings", "آگهی های جذب", "hamkari({'companyid': companyId})","hamkari"],
        ["Can_edit_connections", "مدیریت ارتباطات", "Connections({'companyid': companyId})","Connections"],
        ["Can_edit_productions", "مدیریت محصولات", "products({'companyid': companyId})","products"],
        ["Can_edit_secretriats", "مدیریت دبیرخانه ها", "secretariats({'companyid': companyId})","secretariats"],
        ["Can_edit_BPMS", "مدیریت فرآیندها", "process({'companyid': companyId})","process"],
        ["Can_edit_documents", "مدیریت اسناد", "dms({'companyid': companyId})","dms"],
        ["Can_remove_members", "تعلیق اعضا", "members({'companyid': companyId})","members"],
        ["Can_edit_peoples_to_hire", "گزینش و همکاری", "HamkariJob({'companyid': companyId})","HamkariJob"]
    ]

    def getUserCompanyPermission(self, userID, companyInstance):
        posInstance = PositionsDocument.objects.get(userID=userID, companyID=companyInstance.id)
        if companyInstance.owner_user == userID:
            return self.companyMenuMapping
        result = []
        if "automation" in posInstance.desc:
            if "permission" in posInstance.desc["automation"]:
                for c in self.companyMenuMapping:
                    for pI in posInstance.desc["automation"]["permission"].keys():
                        if c[0] == pI:
                            if posInstance.desc["automation"]["permission"][pI]:
                                result.append(c)
        return result

    def template_page_base(self, request):
        companyProp = PageLoaderApi().getCompanyPropByCompanyID(request, int(request.query_params['id']))
        companyInstance = Company.objects.get(id=int(request.query_params['id']))
        perm = self.getUserCompanyPermission(request.user.id, companyInstance)
        companyProp["sideBarMenu"] = perm
        return render_to_response(
            "companyManagement/CompanyManagement.html",
            companyProp,
            context_instance=RequestContext(self.request))

    @detail_route(methods=['post'])
    def AddMemberToWaitings(self, request, *args, **kwargs):
        companyInstance = Company.objects.get(
            id=self.kwargs["id"])
        chartInstance = Chart.objects.get(id=request.DATA["chartID"])
        profileInstance = Profile.objects.get(id=request.DATA["personID"])
        userInstance = MyUser.objects.get(id=profileInstance.userID)
        self = self
