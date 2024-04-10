import pickle
from bson import ObjectId
from rest_framework_mongoengine.serializers import *
from amspApp.BPMSystem.models import LunchedProcess, LunchedProcessArchive, DoneProcessArchive
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.CompaniesManagment.Processes.serializers.BpmnSerializer import BpmnSerializer
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class DPAInboxSerializer(DynamicFieldsDocumentSerializer):

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = DoneProcessArchive
        fields = (
            'prevPerformer', 'positionName', 'position_id', 'positionPic', 'chartTitle', 'lastUrStepName',
            'id', 'bpmnName', 'name',  'startProcessDate', 'postDate')
        depth = 1

    def create(self, validated_data, **kwargs):
        return 0
