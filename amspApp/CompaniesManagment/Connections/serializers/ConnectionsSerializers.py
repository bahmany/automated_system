import asq
from asq.initiators import query
from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from amspApp.CompaniesManagment.Connections.models import Connections, ConnectionPools
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionDocumentSerializer
from amspApp.CompaniesManagment.Secretariat.models import Secretariat, SecretariatPermissions
from amspApp.CompaniesManagment.models import Company


class ConnectionsSerializer(DocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = Connections

    def save(self, **kwargs):
        if self.data["databaseEngine"] != "mssql":
            raise Exception("This engine is not implemented yet ")
        return super(ConnectionsSerializer, self).save(**kwargs)


class ConnectionPoolSerializer(DocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = ConnectionPools

    dangrousCommands = [
        "import"
    ]

    def save(self, **kwargs):
        checking = self.data["pythonCode"].lower()
        for d in self.dangrousCommands:
            if (checking.find(d)) > -1:
                raise Exception("Using dangrous commands  '" + d + "'")
        for s in self.data["sqls"]:
            if (s["name"].find(" ") > 0):
                raise Exception("SQL commands name must have space between chars '" + s["name"] + "'")
        v = query(self.data["sqls"]).group_by(lambda x: x["name"])
        # checking for duplicate querynames
        res = query([bb.count() for bb in query(self.data["sqls"]).group_by(lambda x: x["name"])]).where(
            lambda x: x > 1).count()
        if res > 0:
            raise Exception("SQL Commads duplicate name error")
        return super(ConnectionPoolSerializer, self).save(**kwargs)
