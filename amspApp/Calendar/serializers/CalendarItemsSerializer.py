from amspApp.Calendar.models import CalendarItems
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer
from rest_framework_mongoengine.serializers import *


class CalendarItemsSerializer(DynamicFieldsDocumentSerializer):
    endDate = serializers.DateTimeField(required=False, allow_null=True)

    detail = serializers.CharField(required=False, allow_null=True)
    finished = serializers.NullBooleanField(required=False,  default=False)
    priority = serializers.IntegerField(required=False, allow_null=True, default=1)  # 1= usual    2= forced
    progress = serializers.IntegerField(required=False, allow_null=True, default=0)
    exp = serializers.DictField(required=False, allow_null=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = CalendarItems



