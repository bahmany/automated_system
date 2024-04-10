from rest_framework_mongoengine.serializers import *

from amspApp.Bpms.models import LunchedProcessArchive, DoneProcessArchive
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class DoneProcessArchiveSerializer(DynamicFieldsDocumentSerializer):

    bpmnName = serializers.CharField(source='bpmn.name', read_only=True)
    bpmnId = serializers.CharField(source='bpmn.id', read_only=True)


    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = DoneProcessArchive
        # fields = (
        #     'id', 'user_id', 'bpmn', 'bpmnName', 'bpmnId', 'thisStep', 'thisPerformer','pastSteps', 'thisStatus', 'name',
        #     'formData')
        depth = 1

    def create(self, validated_data, **kwargs):
        validated_data['user_id'] = str(kwargs['request'].user.pk)
        validated_data['position_id'] = str(PositionsDocument.objects.get(userID=kwargs['request'].user.id,
                                                                      companyID=kwargs[
                                                                          'request'].user.current_company.id).id)
        new = LunchedProcessArchive.objects.create(**validated_data)
        return new
