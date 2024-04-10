from datetime import datetime

from rest_framework import serializers
from rest_framework_mongoengine.serializers import DynamicDocumentSerializer

from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh
from amspApp.Edari.ez.models import Ez, EzSigns


class EzSerializer(DynamicDocumentSerializer):
    JahateAnjameh = serializers.CharField(required=False, allow_null=True)
    Sharh = serializers.CharField(required=False, allow_null=True)

    def to_representation(self, instance):
        result = super(EzSerializer, self).to_representation(instance)
        result["tarikheAnjam"] = mil_to_sh(result.get("tarikheAnjam", datetime.now()))
        return result


    class Meta:
        model = Ez
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

class EzSignsSerializer(DynamicDocumentSerializer):
    class Meta:
        model = EzSigns
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)