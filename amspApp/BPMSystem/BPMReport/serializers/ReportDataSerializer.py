from rest_framework import serializers
from amspApp.BPMSystem.BPMReport.models import ReportTemplate
from amspApp.BPMSystem.models import ReportData
from amspApp.MSSystem.models import MSTemplate
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class ReportDataSerializer(DynamicFieldsDocumentSerializer):
    formData = serializers.SerializerMethodField('get_form_data', read_only=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = ReportData


    def get_form_data(self, obj):
        result = {}
        dataFields = self.dataFields
        for itm in dataFields:
            if itm in obj.formData.keys():
                result[itm] = obj.formData[itm]
        return result
