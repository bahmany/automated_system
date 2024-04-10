import pickle
from bson import ObjectId
from rest_framework_mongoengine.serializers import *
from amspApp.BPMSystem.models import LunchedProcess
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.CompaniesManagment.Processes.serializers.BpmnSerializer import BpmnSerializer
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class LPInboxSerializer(DynamicFieldsDocumentSerializer):
    curAndPrevSteps = serializers.SerializerMethodField('get_current_past_step_name', read_only=True)
    prevPerformer = serializers.SerializerMethodField('get_prev_performer', read_only=True)
    seen = serializers.SerializerMethodField('get_current_seen', read_only=True)
    comeToInbox = serializers.SerializerMethodField('get_come_to_inbox', read_only=True)
    bpmnName = serializers.CharField(source='bpmn.name', read_only=True)
    jobTitle = serializers.CharField(source='name', read_only=True)
    bpmnId = serializers.CharField(source='bpmn.id', read_only=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = LunchedProcess
        fields = (
            'curAndPrevSteps', 'positionName', 'position_id', 'positionName', 'seen', 'comeToInbox','jobTitle',
            'positionPic', 'id', 'postDate', 'bpmnName', 'bpmnId', 'prevPerformer', 'chartTitle')
        depth = 1

    def create(self, validated_data, **kwargs):
        return 0

    def get_private_name(self, obj):
        res = ''
        currentPosition = self.currentPositionObj
        if currentPosition.id == obj.position_id:
            res = obj.name
        return res

    def get_current_past_step_name(self, obj):
        result = {}
        currentPosition = self.currentPositionObj
        if 'thisStepsNames' in obj:
            for itm in obj.thisStepsNames:
                if str(currentPosition.id) in itm.keys():
                    result['current'] = itm[str(currentPosition.id)]
                    result['taskId'] = itm.get("id")
                    result['previous'] = itm['prev']
                    result['chartTitle'] = itm['chartTitle']
                    result['selectedBAM'] = itm.get('selectedBAM',-1)
                    result['selectedBAMDate'] = itm.get('selectedBAMDate',-1)

        return result

    def get_prev_performer(self, obj):
        result = {}
        currentPosition = self.currentPositionObj
        if 'PrevPerformersDetail' in obj:
            for itm in obj.PrevPerformersDetail:
                if str(currentPosition.id) in itm.keys():
                    result['name'] = itm[str(currentPosition.id)]
                    result['avatar'] = itm['avatar']
                    result['chartTitle'] = itm['chartTitle']
                    break

        return result

    def get_current_seen(self, obj):
        result = ''
        currentPosition = self.currentPositionObj
        if 'seen' in obj:
            for itm in obj.seen:
                if str(currentPosition.id) in itm.keys():
                    result = itm[str(currentPosition.id)]
                    break
        return result

    def get_come_to_inbox(self, obj):
        result = ''
        currentPosition = self.currentPositionObj
        if 'lastInboxChangeDate' in obj:
            for itm in obj.lastInboxChangeDate:
                if str(currentPosition.id) in itm.keys():
                    result = itm[str(currentPosition.id)]

        return result

