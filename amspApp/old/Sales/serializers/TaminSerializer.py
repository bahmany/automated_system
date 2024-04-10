from rest_framework import serializers

from amspApp.Sales.models import TaminProject, TaminDetails
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class TaminProjectSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = TaminProject

    depth = 1


class TaminDetailsSerializer(DynamicFieldsDocumentSerializer):

    mahaleAnbar = serializers.CharField(required=False, allow_null=True)
    dasteBandiKharid = serializers.IntegerField(required=False, allow_null=True)
    somarehSefaresh = serializers.CharField(required=False, allow_null=True)
    tarikheVoroodBeGomrok = serializers.DateTimeField(required=False, allow_null=True)
    tarikheBoresh = serializers.DateTimeField(required=False, allow_null=True)
    masraf = serializers.CharField(required=False, allow_null=True)
    toozihateKeifi = serializers.CharField(required=False, allow_null=True)
    toozihateBarnameRizi = serializers.CharField(required=False, allow_null=True)
    tozihat = serializers.CharField(required=False, allow_null=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = TaminDetails

    depth = 1
