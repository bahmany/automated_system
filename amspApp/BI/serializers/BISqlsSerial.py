from amspApp.BI.DataTables.models import DataTable
from amspApp.BI.models import BISqls
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer
from rest_framework import serializers


class BISqlsSerializers(DynamicFieldsDocumentSerializer):
    def_name = serializers.CharField(allow_null=True, allow_blank=True, required=False,
                                     max_length=255)  # when type_of_datasource = 4
    datatable_id = serializers.PrimaryKeyRelatedField(queryset=DataTable.objects.all(), required=False, allow_null=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = BISqls
        depth = 1


class BISqlsLess1Serializers(DynamicFieldsDocumentSerializer):

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = BISqls
        depth = 1
        fields = ('id', 'sqlTitle')
