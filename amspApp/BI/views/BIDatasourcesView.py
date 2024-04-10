from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.BI.airflowconnector import AirflowConnector
from amspApp.BI.models import BIDatasource
from amspApp.BI.serializers.BIDatasourceSerial import BIDatasourceSerializers
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class BIDatasourcesViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = BIDatasource.objects.all().order_by('-id')
    serializer_class = BIDatasourceSerializers

    def initial(self, request, *args, **kwargs):
        airflow = AirflowConnector()
        airflow.get_list('connections')

        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            # _mutable = request.data._mutable
            # request.data._mutable = True
            request.data["positionID"] = posiIns.positionID
            # request.data._mutable = _mutable
        return super(BIDatasourcesViewSet, self).initial(request, *args, **kwargs)

    @list_route(methods=['GET'])
    def get_list(self, request, *args, **kwargs):
        airflow = AirflowConnector()
        result = airflow.get_list('connections')['connections']
        for r in result:
            result_ins = BIDatasource.objects.filter(airflow_connection_id=r['connection_id']).first()
            if result_ins:
                r['datasourceTitle'] = result_ins.datasourceTitle
                r['id'] = result_ins.id
            else:
                r['datasourceTitle'] = 'بی نام'
        return Response(result)

    """
    AirflowConnector().post('connections/test', {'conn_type': 'mssql', 'connection_id': 'connect_to_rahkaran', 'host': '172.16.5.12', 'login': 'bahmany', 'schema': 'master', 'port': 1433, 'password': '****', 'extra': ''})
    """

    def convert_package_name_to_hook_type(self, package_name):
        if package_name == "apache-airflow-providers-ftp": return "ftp"
        if package_name == "apache-airflow-providers-http": return "http"
        if package_name == "apache-airflow-providers-imap": return "imap"
        if package_name == "apache-airflow-providers-microsoft-mssql": return "mssql"
        if package_name == "apache-airflow-providers-sqlite": return "sqlite"
        if package_name == "": return ""

    @detail_route(methods=['GET'])
    def test_connection(self, request, *args, **kwargs):
        datasource_interface = self.queryset.get(id=kwargs['id'])
        del datasource_interface.details['datasourceTitle']
        del datasource_interface.details['positionID']
        datasource_interface.details['conn_type'] = self.convert_package_name_to_hook_type(
            datasource_interface.details['conn_type'])
        result = AirflowConnector().post('connections/test', datasource_interface.details)
        if result.text.find('succ') > 0:
            return Response({"msg": "succ"})
        return Response({"msg": "err"})

    def create(self, request, *args, **kwargs):
        dt = {
            'datasourceTitle': request.data['datasourceTitle'],
            'details': request.data,
            'positionID': GetPositionViewset().GetCurrentPositionDocumentInstance(request).positionID,
            'airflow_connection_id': request.data['connection_id'],
        }
        ser = self.serializer_class(data=dt)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @list_route(methods=['GET'])
    def get_providers(self, request, *args, **kwargs):
        airflow = AirflowConnector()
        result = airflow.get_list('providers')
        return Response(result)

    @detail_route(methods=['PATCH'])
    def change_name(self, request, *args, **kwargs):
        if kwargs['id'] == "undefined":
            kwargs['id'] = None
        result_ins = BIDatasource.objects.filter(airflow_connection_id=request.data['connection_id']).first()
        if result_ins is None:
            dt = {
                'datasourceTitle': request.data['datasourceTitle'],
                'details': {},
                'positionID': request.data['positionID'],
                'airflow_connection_id': request.data['connection_id'],
            }
            cc = self.serializer_class(data=dt)
            cc.is_valid(raise_exception=True)
            cc.save()
            return Response(cc.data)
        else:
            dt = {
                'datasourceTitle': request.data['datasourceTitle'],
                'positionID': request.data['positionID'],
            }
            instance = self.queryset.get(airflow_connection_id=request.data['connection_id'])
            cc = self.serializer_class(instance=instance, data=dt, partial=True)
            cc.is_valid(raise_exception=True)
            cc.save()
            return Response(cc.data)
