import pickle
from bson import ObjectId
from rest_framework_mongoengine.serializers import *
from amspApp.BPMSystem.models import LunchedProcess
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.CompaniesManagment.Processes.serializers.BpmnSerializer import BpmnSerializer
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class ShowDiagramSerializer(DynamicFieldsDocumentSerializer):
    curAndPrevSteps = serializers.SerializerMethodField('get_current_past_step_name', read_only=True)
    # prevPerformer = serializers.SerializerMethodField('get_prev_performer', read_only=True)
    # seen = serializers.SerializerMethodField('get_current_seen', read_only=True)
    # comeToInbox = serializers.SerializerMethodField('get_come_to_inbox', read_only=True)
    # formSchema = serializers.SerializerMethodField('get_form_schema', read_only=True)
    # formData = serializers.SerializerMethodField('get_form_data', read_only=True)
    bpmnName = serializers.CharField(source='bpmn.name', read_only=True)
    bpmnForm= serializers.ListField(source='bpmn.form', read_only=True)
    xml = serializers.CharField(source='bpmn.xml', read_only=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = LunchedProcess
        fields = (
            'xml', 'bpmnName','thisSteps','pastSteps','bpmnForm','curAndPrevSteps')
        depth = 1

    def create(self, validated_data, **kwargs):
        return 0
    #
    def get_current_past_step_name(self, obj):
        result = {}
        currentPosition = self.currentPositionObj
        if 'thisStepsNames' in obj:
            for itm in obj.thisStepsNames:
                if str(currentPosition.id) in itm.keys():
                    result['current'] = itm[str(currentPosition.id)]
                    result['previous'] = itm['prev']

        return result
    #
    # def get_prev_performer(self, obj):
    #     result = {}
    #     currentPosition = self.currentPositionObj
    #     if 'PrevPerformersDetail' in obj:
    #         for itm in obj.PrevPerformersDetail:
    #             if str(currentPosition.id) in itm.keys():
    #                 result['name'] = itm[str(currentPosition.id)]
    #                 result['avatar'] = itm['avatar']
    #
    #     return result
    #
    # def get_come_to_inbox(self, obj):
    #     result = ''
    #     currentPosition = self.currentPositionObj
    #     if 'lastInboxChangeDate' in obj:
    #         for itm in obj.lastInboxChangeDate:
    #             if str(currentPosition.id) in itm.keys():
    #                 result = itm[str(currentPosition.id)]
    #
    #     return result
    #
    # def get_form_schema(self, obj):
    #     result = {}
    #     currentStep = ''
    #     currentPosition = self.currentPositionObj
    #     formsList = obj.bpmn['form']
    #     if 'thisSteps' in obj:
    #         for itm in obj.thisSteps:
    #             if str(currentPosition.id) in itm.keys():
    #                 currentStep = itm[str(currentPosition.id)]
    #                 break
    #     for itm in formsList:
    #         if itm['bpmnObjID'] == currentStep:
    #             result = itm['schema']
    #             break
    #     return result
    #
    # def get_form_data(self, obj):
    #     result = {}
    #     currentStep = ''
    #     fieldsList = []
    #     currentPosition = self.currentPositionObj
    #     formsList = obj.bpmn['form']
    #     formsData = obj.formData
    #     if 'thisSteps' in obj:
    #         for itm in obj.thisSteps:
    #             if str(currentPosition.id) in itm.keys():
    #                 currentStep = itm[str(currentPosition.id)]
    #                 break
    #     for itm in formsList:
    #         if itm['bpmnObjID'] == currentStep:
    #             fieldsList = itm['schema']['fields']
    #             break
    #
    #     for itm in fieldsList:
    #         if itm['name'] in formsData.keys():
    #             result[itm['name']] = formsData[itm['name']]
    #
    #     return result
