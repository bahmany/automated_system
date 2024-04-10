import pickle
from bson import ObjectId
from rest_framework_mongoengine.serializers import *
from amspApp.BPMSystem.models import LunchedProcess, LunchedProcessArchive
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.CompaniesManagment.Processes.serializers.BpmnSerializer import BpmnSerializer
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class TrackLPASerializer(DynamicFieldsDocumentSerializer):
    # curAndPrevSteps = serializers.SerializerMethodField('get_current_past_step_name', read_only=True)
    # prevPerformer = serializers.SerializerMethodField('get_prev_performer', read_only=True)
    # seen = serializers.SerializerMethodField('get_current_seen', read_only=True)
    # comeToInbox = serializers.SerializerMethodField('get_come_to_inbox', read_only=True)
    # formSchema = serializers.SerializerMethodField('get_form_schema', read_only=True)
    # formData = serializers.SerializerMethodField('get_form_data', read_only=True)
    bpmnName = serializers.CharField(source='bpmn.name', read_only=True)
    xml = serializers.CharField(source='bpmn.xml', read_only=True)
    # form = serializers.ListField(source='bpmn.form', read_only=True)
    realPastSteps = serializers.SerializerMethodField('get_real_past_step', read_only=True)
    form = serializers.SerializerMethodField('get_real_form', read_only=True)
    exactThisStep = serializers.SerializerMethodField('get_exact_this_step', read_only=True)
    # formData = serializers.SerializerMethodField('get_real_form_data', read_only=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = LunchedProcessArchive
        fields = (
            'xml', 'bpmnName', 'steps', 'realPastSteps','form','formData','exactThisStep')
        depth = 1

    def create(self, validated_data, **kwargs):
        return 0

    def get_real_past_step(self, obj):
        res = LunchedProcess.objects.get(id=obj.lunchedProcessId).pastSteps
        return res
    def get_exact_this_step(self, obj):
        stepsList = LunchedProcess.objects.get(id=obj.lunchedProcessId).thisStepsNames
        res =[]
        for itm in stepsList:
            if not itm['id'] in res:
                res.append(itm['id'])
        return res

    def get_real_form(self, obj):
        res=[]
        formsList = obj.bpmn['form']
        if 'steps' in obj:
            for itm in formsList:
                if itm['bpmnObjID'] in obj.steps:
                    res.append(itm)
        return res