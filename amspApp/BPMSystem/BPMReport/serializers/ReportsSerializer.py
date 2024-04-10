from rest_framework import serializers
from amspApp.BPMSystem.BPMReport.models import ReportTemplate
from amspApp.MSSystem.models import MSTemplate
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class ReportsSerializer(DynamicFieldsDocumentSerializer):
    name = serializers.CharField(label="name", required=True, allow_null=False)
    publishedUsers = serializers.ListField(label="publishedUsers", required=False, allow_null=True)
    publishedUsersDetail = serializers.ListField(label="publishedUsersDetail", required=False, allow_null=True)
    icon = serializers.CharField(label="icon", required=True, allow_null=False)
    desc = serializers.CharField(label="desc", required=False, allow_null=True, allow_blank=True)
    dataType = serializers.CharField(label="dataType", required=True, allow_null=False)
    companyId = serializers.IntegerField(label="companyId", required=False, allow_null=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = MSTemplate


class ReportTemplateSerializer(DynamicFieldsDocumentSerializer):
    # name = serializers.CharField(label="name", read_only=True)
    # icon = serializers.CharField(label="icon", read_only=True)
    # desc = serializers.CharField(label="desc", read_only=True)
    # dataType = serializers.CharField(label="dataType", read_only=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = ReportTemplate
        # fields = ('name', 'icon', 'desc', 'dataType', 'id')
