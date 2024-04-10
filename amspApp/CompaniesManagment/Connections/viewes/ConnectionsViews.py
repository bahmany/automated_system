import os

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
import pymssql
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from amspApp.CompaniesManagment.Connections.models import Connections
from amspApp.CompaniesManagment.Connections.serializers.ConnectionsSerializers import ConnectionsSerializer
from amspApp.CompaniesManagment.Positions.models import Position
from amspApp.CompaniesManagment.Secretariat.models import Secretariat, SecretariatPermissions
from amspApp.CompaniesManagment.Secretariat.serializers.SecretariatsSerializers import SecretariatSerializer, \
    SecretariatSerializerPermission
from amspApp.CompaniesManagment.models import Company
from amspApp.CompaniesManagment.permissions.CompanyPermissions import CanCruid
from amspApp.CompaniesManagment.permissions.PermissionChecker import get_permissions
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh, mil_to_sh_with_time
from amspApp._Share.ListPagination import ListPagination


class ConnectionsViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Connections.objects.all()
    serializer_class = ConnectionsSerializer
    pagination_class = ListPagination
    permission_name = "Can_edit_connections"
    permission_classes = (CanCruid,)

    def get_permissions(self):
        return get_permissions(self, ConnectionsViewSet)

    def template_page(self, request, *args, **kwargs):
        return render_to_response("companyManagement/Connections/base.html", {},
                                  context_instance=RequestContext(self.request))

    def create(self, request, *args, **kwargs):
        request.data["userID"] = request.user.id
        request.data["companyID"] = kwargs["companyID_id"]  # has security bug and must be correct later
        return super(ConnectionsViewSet, self).create(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        if (self.kwargs.get("companyID_id")):
            if (self.kwargs.get("companyID_id") != "undefined"):
                queryset = queryset.filter(companyID=int(self.kwargs["companyID_id"]))
                return queryset
        return []

    @list_route(methods=["post"])
    def testConnection(self, request, *args, **kwargs):
        # if self:
        #     return Response({}) # disabled for sec porpose
        hostAddress = request.data["hostAddress"]  # +":"+request.data["hostAddress"]
        username = request.data["username"]
        password = request.data["password"]
        databaseName = request.data["databaseName"]

        # try:
        os.environ['TDSDUMP'] = 'stdout'
        conn = pymssql.connect(server=hostAddress, user=username, password=password, database=databaseName)
        cursor = conn.cursor(as_dict=True)
        # except:
        #     raise Exception("Connection to mssql failure")

        return Response({"ok": "ok"})

    def getConnection(self, connectionInstance):
        # if self:
        #     return Response({}) # disabled for sec porpose

        os.environ['TDSDUMP'] = 'stdout'
        try:
            conn = pymssql.connect(server=connectionInstance.hostAddress,
                                   user=connectionInstance.username,
                                   password=connectionInstance.password,
                                   database=connectionInstance.databaseName,
                                   # charset="UTF-8",
                                   as_dict=True)
        except:
            raise Exception("No connection to pool mrb %s %s" % (connectionInstance.hostAddress,connectionInstance.databaseName,))
        cursor = conn.cursor(as_dict=True)
        return cursor


    def getConnectionAutoCommit(self, connectionInstance):
        # if self:
        #     return Response({}) # disabled for sec porpose

        os.environ['TDSDUMP'] = 'stdout'
        try:
            conn = pymssql.connect(server=connectionInstance.hostAddress,
                                   user=connectionInstance.username,
                                   password=connectionInstance.password,
                                   database=connectionInstance.databaseName,
                                   charset="UTF-8",
                                   as_dict=True)
            conn.autocommit(True)

        except:
            raise Exception("No connection to pool mrb %s %s" % (connectionInstance.hostAddress,connectionInstance.databaseName,))
        cursor = conn.cursor(as_dict=True)
        return cursor

    def getConnectionAutoCommit1(self, connectionInstance):
        # if self:
        #     return Response({}) # disabled for sec porpose

        os.environ['TDSDUMP'] = 'stdout'
        try:
            conn = pymssql.connect(server=connectionInstance.hostAddress,
                                   user=connectionInstance.username,
                                   password=connectionInstance.password,
                                   database=connectionInstance.databaseName,
                                   charset="UTF-8",
                                   autocommit = True,
                                   as_dict=True)
            # conn.autocommit(1)

        except:
            raise Exception("No connection to pool mrb %s %s" % (connectionInstance.hostAddress,connectionInstance.databaseName,))
        cursor = conn.cursor(as_dict=True)
        return cursor



    def getConnectionRaw(self, connectionInstance):
        # if self:
        #     return Response({}) # disabled for sec porpose

        os.environ['TDSDUMP'] = 'stdout'
        try:
            conn = pymssql.connect(server=connectionInstance.hostAddress,
                                   user=connectionInstance.username,
                                   password=connectionInstance.password,
                                   database=connectionInstance.databaseName,
                                   charset="UTF-8",
                                   as_dict=False)
        except:
            raise Exception("No connection to pool mrb %s %s" % (connectionInstance.hostAddress,connectionInstance.databaseName,))
        cursor = conn.cursor(as_dict=False)
        return cursor
