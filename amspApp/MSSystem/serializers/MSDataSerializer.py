from datetime import datetime

from rest_framework import serializers
from amspApp.MSSystem.models import MSTemplate, MSData
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class MSDataSerializer(DynamicFieldsDocumentSerializer):
    value = serializers.IntegerField(label="value", write_only=True, required=True, allow_null=False)
    desc = serializers.CharField(label="desc", write_only=True, required=False, allow_null=True, allow_blank=True)
    entryDate = serializers.DateTimeField(label="entryDate", write_only=True, required=True, allow_null=False)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = MSData

class MSDataInboxSerializer(DynamicFieldsDocumentSerializer):
    value = serializers.CharField(label="value", read_only=True)
    entryDate = serializers.DateTimeField(label="entryDate", read_only=True)
    postDate = serializers.DateTimeField(required=False, default=datetime.now())
    desc = serializers.CharField(label="desc", read_only=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = MSData
        fields=('value','entryDate',"postDate",'desc','id')