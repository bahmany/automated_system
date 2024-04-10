from rest_framework_mongoengine.serializers import *

from amspApp.BI.DataTables.models import DataTableValues, TemporaryDataTableValuesForProcess, DataTable
from amspApp.BI.DataTables.viewer.DataTablePythonScriptRunner import DataTablePythonScriptRunner


class DataTableValuesSerializer(DocumentSerializer):
    desc = serializers.CharField(required=False, allow_null=True)
    exp = serializers.DictField(required=False, allow_null=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = DataTableValues

    def create(self, validated_data):
        # getting datatable instance
        dataTableInstance = DataTable.objects.get(id=validated_data['dataTableLink'])
        # running python triggers
        runner = DataTablePythonScriptRunner(dataTableInstance)
        runner.doBeforeInsert(dataTableInstance.exp.get('beforecreate'), validated_data)
        result = super(DataTableValuesSerializer, self).create(validated_data)
        # running python triggers
        runner.doAfterInsert(dataTableInstance.exp.get('aftercreate'), result)
        return result


class TemporaryDataTableValuesForProcessSerializer(DocumentSerializer):
    desc = serializers.CharField(required=False, allow_null=True)
    exp = serializers.DictField(required=False, allow_null=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = TemporaryDataTableValuesForProcess
