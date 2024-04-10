from rest_framework import serializers

from amspApp.QC.models import Finding
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class FindingSerializer(DynamicFieldsDocumentSerializer):
    currentPerformerPositionID = serializers.IntegerField(label="desc", required=False, allow_null=True)
    performers = serializers.DictField(label="desc", required=False, allow_null=True)
    desc = serializers.DictField(label="desc", required=False, allow_null=True)
    Files = serializers.DictField(label="desc", required=False, allow_null=True)
    dueDateStart = serializers.DateTimeField(label="desc", required=False, allow_null=True)
    dueDateEnd = serializers.DateTimeField(label="desc", required=False, allow_null=True)
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = Finding