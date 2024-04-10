
from rest_framework_mongoengine.serializers import DynamicDocumentSerializer

from amspApp.ControlProject.models import  CalYearsShare


class ControlProjectYearsShareSerializer(DynamicDocumentSerializer):

    # postDate = serializers.DateTimeField(default=datetime.now())
    # startDate = serializers.DateTimeField(required=True)
    # endDate = serializers.DateTimeField(required=True)
    # positionID = serializers.IntegerField(required=True)
    # companyID = serializers.IntegerField(required=True)
    # title = serializers.CharField(required=True)
    # desc = serializers.CharField(required=False, allow_null=True)
    # exp = serializers.DictField(required=False, allow_null=True)

    class Meta:
        model = CalYearsShare
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)



