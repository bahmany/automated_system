from bson import ObjectId
from rest_framework_mongoengine.serializers import *

from amspApp.BPMSystem.models import LunchedProcess
from amspApp.BPMSystem.serializers.ProcessFormAdvanceTableSerializer import ProcessFormAdvanceTableSerializer
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.CompaniesManagment.Processes.serializers.BpmnSerializer import BpmnSerializer
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class LunchedProcessSerializer(DynamicFieldsDocumentSerializer):
    bpmnForCreate = serializers.CharField(label="bpmn",
                                          style={'template': 'forms/base-templates/selectAngular.html',
                                                 'cssclass': 'col-md-12', 'ngmodel': 'lunchedProcess.bpmnForCreate',
                                                 'ngoptions': 'obj.id as obj.name for obj in bpmns'}, write_only=True)

    name = serializers.CharField(label="name", style={'template': 'forms/base-templates/input.html',
                                                      'cssclass': 'col-md-12',
                                                      'ngmodel': 'lunchedProcess.name'})

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = LunchedProcess
        depth = 1

    def handleAdvanceTables(self, validated_data):
        prc = validated_data["bpmn"]
        for_item = 0
        for item in prc["form"]:
            for_item += 1
            for_it = 0
            for it in item["schema"]["fields"]:
                for_it += 1
                if it["type"] == "advancetable":
                    dt = {}
                    dt["position_id"] = validated_data["position_id"]
                    dt["bpmsID"] = ObjectId(validated_data["bpmn"]["id"])
                    # dt["processID"] = validated_data.id
                    # dt["fieldID"] = validated_data.id
                    dt["table"] = {}
                    dt["fieldID"] = it["name"]
                    dt["table"]["fields"] = []
                    for_dhead = 0
                    itemsinthead = list(it["thead"].keys())
                    itemsinthead.sort()
                    for dhead in itemsinthead:
                        for_dhead += 1
                        tbl = {}
                        tbl["name"] = it["thead"][dhead]["name"] if "name" in it["thead"][dhead] else None
                        tbl["inlineStyle"] = it["thead"][dhead]["inlineStyle"] if "inlineStyle" in it["thead"][
                            dhead] else None
                        tbl["fieldType"] = it["thead"][dhead]["fieldType"] if "fieldType" in it["thead"][
                            dhead] else None
                        tbl["elementAttrs"] = it["thead"][dhead]["elementAttrs"] if "elementAttrs" in it["thead"][
                            dhead] else None
                        tbl["cssClasses"] = it["thead"][dhead]["cssClasses"] if "cssClasses" in it["thead"][
                            dhead] else None
                        tbl["lookupDatatable"] = it["thead"][dhead]["lookupDatatable"] if "lookupDatatable" in \
                                                                                          it["thead"][
                                                                                              dhead] else None  # table name - displayfield;displayfield;displayfield - return valu1
                        dt["table"]["fields"].append(tbl)
                    serial = ProcessFormAdvanceTableSerializer(data=dt)
                    serial.is_valid(raise_exception=True)
                    serial = serial.save()
                    it["tableID"] = str(serial.id)

        return validated_data

    def create(self, validated_data, **kwargs):
        validated_data['user_id'] = int(kwargs['request'].user.pk)
        validated_data['bpmn'] = BpmnSerializer(Bpmn.objects.get(id=validated_data['bpmnForCreate'])).data
        current_pos = PositionsDocument.objects.get(userID=kwargs['request'].user.id,
                                                    companyID=kwargs['request'].user.current_company.id)
        validated_data['position_id'] = current_pos.id
        validated_data['StepHistory'] = []
        validated_data['positionName'] = current_pos.profileName
        validated_data['positionPic'] = current_pos.avatar
        validated_data['chartId'] = current_pos.chartID
        validated_data['chartTitle'] = current_pos.chartName
        validated_data = self.handleAdvanceTables(validated_data=validated_data)
        if 'parentId' in validated_data:
            validated_data['name'] = validated_data['bpmn']['name'] + ' از ' + validated_data['parentBpmnName']
        new = LunchedProcess.objects.create(**validated_data)

        return new

    def createFromCallActivity(self, validated_data, **kwargs):
        validated_data['user_id'] = int(kwargs['parentObj'].user_id)
        validated_data['bpmn'] = BpmnSerializer(Bpmn.objects.get(id=validated_data['bpmnForCreate'])).data
        Starter_pos = PositionsDocument.objects.get(id=kwargs['parentObj'].position_id)
        prev_pos = PositionsDocument.objects.get(userID=kwargs['request'].user.id,
                                                 companyID=kwargs[
                                                     'request'].user.current_company.id)

        validated_data['position_id'] = Starter_pos.id
        validated_data['positionName'] = Starter_pos.profileName
        validated_data['positionPic'] = Starter_pos.avatar
        validated_data['chartId'] = Starter_pos.chartID
        validated_data['chartTitle'] = Starter_pos.chartName
        if 'parentId' in validated_data:
            validated_data['name'] = validated_data['bpmn']['name'] + ' از ' + validated_data['parentBpmnName']
        new = LunchedProcess.objects.create(**validated_data)

        return new
