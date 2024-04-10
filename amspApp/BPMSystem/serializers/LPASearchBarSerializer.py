import pickle
from bson import ObjectId
from rest_framework_mongoengine.serializers import *
from amspApp.BPMSystem.models import LunchedProcess
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.CompaniesManagment.Processes.serializers.BpmnSerializer import BpmnSerializer
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class ShowFormSerializer(DynamicFieldsDocumentSerializer):
    curAndPrevSteps = serializers.SerializerMethodField('get_current_past_step_name', read_only=True)

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = LunchedProcess
        fields = (
            'curAndPrevSteps', 'positionName', 'position_id', 'name', 'positionName', 'comeToInbox',
            'positionPic', 'id', 'postDate', 'bpmnName', 'prevPerformer', 'formSchema', 'formData','chartTitle','seen')
        depth = 1

    def create(self, validated_data, **kwargs):
        return 0

    def get_current_past_step_name(self, obj):
        result = {}
        currentPosition = self.currentPositionObj
        if 'thisStepsNames' in obj:
            for itm in obj.thisStepsNames:
                if str(currentPosition.id) in itm.keys():
                    result['current'] = itm[str(currentPosition.id)]
                    result['previous'] = itm['prev']

        return result
