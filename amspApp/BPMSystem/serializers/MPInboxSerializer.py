import pickle
from bson import ObjectId
from rest_framework_mongoengine.serializers import *
from amspApp.BPMSystem.models import LunchedProcess, LunchedProcessMessages
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.CompaniesManagment.Processes.serializers.BpmnSerializer import BpmnSerializer
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class MPInboxSerializer(DynamicFieldsDocumentSerializer):
    bpmnName = serializers.CharField(source='bpmn.name', read_only=True)
    bpmnId = serializers.CharField(source='bpmn.id', read_only=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = LunchedProcessMessages
        fields = (
            'id',
            'positionName',
            'positionPic',
            'chartTitle',
            'bpmnName',
            'name',
            'bpmnId',
            'thisStepName',
            'prevStepName',
            'startProcessDate',
            'performerDetail',
            'seen',
            'postDate'
            )

    def create(self, validated_data, **kwargs):
        return 0




