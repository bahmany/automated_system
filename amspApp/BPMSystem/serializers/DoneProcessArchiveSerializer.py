import pickle
from bson import ObjectId
from rest_framework_mongoengine.serializers import *
from amspApp.BPMSystem.models import LunchedProcess, LunchedProcessArchive, DoneProcessArchive
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class DoneProcessArchiveSerializer(DynamicFieldsDocumentSerializer):

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = DoneProcessArchive

    # def create(self, validated_data, **kwargs):
    #     validated_data['user_id'] = str(kwargs['request'].user.pk)
    #     validated_data['position_id'] = str(PositionsDocument.objects.get(userID=kwargs['request'].user.id,
    #                                                                   companyID=kwargs[
    #                                                                       'request'].user.current_company.id).id)
    #     return super(DoneProcessArchiveSerializer,self).create(validated_data)
