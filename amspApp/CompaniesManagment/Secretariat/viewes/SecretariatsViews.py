from symbol import decorators

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from amspApp.CompaniesManagment.Positions.models import Position
from amspApp.CompaniesManagment.Secretariat.models import Secretariat, SecretariatPermissions
from amspApp.CompaniesManagment.Secretariat.serializers.SecretariatsSerializers import SecretariatSerializer, \
    SecretariatSerializerPermission
from amspApp.CompaniesManagment.models import Company
from amspApp.CompaniesManagment.permissions.CompanyPermissions import CanCruid
from amspApp.CompaniesManagment.permissions.PermissionChecker import get_permissions
from amspApp._Share.ListPagination import ListPagination
from amspApp.amspUser.models import MyUser


class SecretariatsViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Secretariat.objects.all()
    serializer_class = SecretariatSerializer
    pagination_class = ListPagination
    permission_name = "Can_edit_secretriats"
    permission_classes = (CanCruid,)


    def get_permissions(self):
        return get_permissions(self, SecretariatsViewSet)
    # filter_backends = (filters.DjangoFilterBackend,)


    # def initialize_request(self, request, *args, **kwargs):
    #     result = super(SecretariatsViewSet, self).initialize_request(request, *args, **kwargs)
    #
    #     return result
    #
    # def initial(self, request, *args, **kwargs):
    #     self = self


    def get_queryset(self):
        companyInstance = Company.objects.get(
            id=self.kwargs["companyID_id"],
            owner_user=self.request.user.id)
        self.queryset = Secretariat.objects.filter(company=companyInstance).order_by("-id")
        return super(SecretariatsViewSet, self).get_queryset()

    def create(self, request, *args, **kwargs):
        return super(SecretariatsViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        companyInstance = Company.objects.get(
            id=self.kwargs["companyID_id"],
            owner_user=self.request.user.id)
        secInstance = Secretariat.objects.get(id=self.kwargs["id"])

        if secInstance.set_SecretariatPermissions.count() != 0:
            raise Exception()

        return super(SecretariatsViewSet, self).destroy(request, *args, **kwargs)


    # def GetDefaultSecretariatInstanceByID(self, PositionChartID):
    # return SecretariatPermissions.objects.get(
    #         chart=PositionChartID,
    #         permission__startswith="1",
    #         default = True
    #     )

    def GetDefaultSecretariatInstanceByPositionInstance(self, positionInstance):
        result = SecretariatPermissions.objects.filter(
            chart_id=positionInstance.chart_id,
            permission__startswith="1",
            default=True).order_by("-id")

        # this is for when user has no dabir in current company
        # when we send letter to a person who has no default dabir
        # system automatically creates a default dabir permission and add
        # first secretariat for its permission
        if result.count() == 0:
            def_sec = Secretariat.objects.filter(company_id=positionInstance.company_id)[0]
            dt = {
                "chart": positionInstance.chart_id,
                "permission":"100",
                "default":True,
                "secretariat":def_sec.id
            }
            sp = SecretariatSerializerPermission(data=dt)
            sp.is_valid(raise_exception=True)
            sp = sp.save()
            return sp

            pass

        # if result.count() > 1:
        #     raise Exception()


        return result[0]
    def GetDefaultSecretariatInstance(self, request):
        positionInstance = Position.objects.get(user=request.user, company=request.user.current_company)
        companyInstance = positionInstance.company
        return SecretariatPermissions.objects.get(
            chart=positionInstance.chart_id,
            permission__startswith="1",
            default=True
        )
    def GetDefaultSecretariatInstanceByUserID(self, userID):
        currentCompany = MyUser.objects.get(id = userID).current_company
        positionInstance = Position.objects.get(user=userID, company=currentCompany)
        companyInstance = positionInstance.company
        return SecretariatPermissions.objects.get(
            chart=positionInstance.chart_id,
            permission__startswith="1",
            default=True
        )



    @list_route(methods=["get"])
    def GetAllPermitted(self, request, *args, **kwargs):
        positionInstance = Position.objects.get(user=request.user, company=request.user.current_company)
        companyInstance = positionInstance.company
        # self.get_queryset()
        secretariats = Secretariat.objects.filter(company=companyInstance)
        secretariatsPermission = SecretariatPermissions.objects.filter(
            secretariat__in=secretariats,
            chart=positionInstance.chart_id,
            permission__startswith="1"
        )
        secretariatsPermissionList = list(secretariatsPermission.values())
        secretariatsList = list(secretariats)

        # putting secretariat name to secretariatPermissions :))
        for s in secretariatsPermissionList:
            for sl in secretariatsList:
                if s['secretariat_id'] == sl.id:
                    s["name"] = sl.name
        result = [{
                      "default": s["default"],
                      "name": s["name"],
                      "id": s["id"],
                      "secretariat_id": s["secretariat_id"]
                  } for s in secretariatsPermissionList]

        return Response(result)

    # @decorators.permission_classes((IsAuthenticated,))
    @list_route(methods=["post"])
    def ChangeDefault(self, request, *args, **kwargs):
        positionInstance = Position.objects.get(user=self.request.user, company=self.request.user.current_company)
        companyInstance = positionInstance.company

        secretariat = Secretariat.objects.get(id=request.data["secretariat_id"])
        selectedSecInstance = SecretariatPermissions.objects.get(
            secretariat=secretariat,
            chart=positionInstance.chart_id,
            permission__startswith="1"
        )
        secretariats = Secretariat.objects.filter(company=companyInstance)
        secretariatsPermission = SecretariatPermissions.objects.filter(
            secretariat__in=secretariats,
            chart=positionInstance.chart_id,
            permission__startswith="1"
        )
        for s in secretariatsPermission:
            s.default = False
            s.save()
        selectedSecInstance.default = True
        selectedSecInstance.save()

        return Response({})


    def template_page(self, request, *args, **kwargs):
        return render_to_response("companyManagement/Secretarait.html", {},
                                  context_instance=RequestContext(self.request))
