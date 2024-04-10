from amspApp.Letter.models import CompanyRecieverGroup, CompanyReciever, Letter, Recieved, ExportScannedAfterSend, \
    ExportTemplates
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer
from bson import ObjectId
from rest_framework_mongoengine.serializers import *

__author__ = 'mohammad'


class CompanyRecieverGroupSerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = CompanyRecieverGroup

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class CompanyRecieverSerializer(DynamicFieldsDocumentSerializer):
    # group = serializers.Ref
    class Meta:
        model = CompanyReciever
        depth = 0

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class RecievedSerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = Recieved

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class ExportScannedAfterSendSerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = ExportScannedAfterSend

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class ExportTemplatesSerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = ExportTemplates

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)
