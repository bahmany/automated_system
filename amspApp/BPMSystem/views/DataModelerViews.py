# import xmltodict as xd
import xml.etree.ElementTree as ET

from SpiffWorkflow.bpmn.parser.util import xpath_eval
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.CompaniesManagment.Processes.serializers.BpmnSerializer import BpmnSerializer


class DataModelerViewSet(viewsets.ModelViewSet):
    # lookup_field = 'id'
    # queryset = LunchedProcess.objects.all()
    # serializer_class = LunchedProcessSerializer
    # pagination_class = UserListPagination
    # renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)

    @list_route(methods=["post"])
    def removeFromCurrentTask(self, request, *args, **kwargs):
        bpmnInstance = Bpmn.objects.get(id=request.data.get("bpmnID"))
        bpmnSerial = BpmnSerializer(instance=bpmnInstance).data

        objNameToRemove = request.data.get("fieldName")

        processObjs = bpmnSerial["processObjs"]
        form = bpmnSerial["form"]

        index = -1
        indx = -1
        for obj in processObjs:
            indx += 1
            if obj['name'] == objNameToRemove:
                index = indx
        if index > -1:
            del processObjs[index]

        for f in form:
            if f["bpmnObjID"] == request.data.get("taskID"):
                indx = -1
                index = -1
                for field in f["schema"]["fields"]:
                    indx += 1
                    if field["name"] == objNameToRemove:
                        index = indx
                if index > -1:
                    del f["schema"]["fields"][index]

                for l in f["schema"]["layout"]:
                    if l.get("layout"):
                        if l.get("layout").get("row1"):
                            if l.get("layout").get("row1").get("name") == objNameToRemove:
                                l.get("layout")["row1"] = {}

                        if l.get("layout").get("row2"):
                            if l.get("layout").get("row2").get("name") == objNameToRemove:
                                l.get("layout")["row2"] = {}

                        if l.get("layout").get("row3"):
                            if l.get("layout").get("row3").get("name") == objNameToRemove:
                                l.get("layout")["row3"] = {}

                        if l.get("layout").get("row4"):
                            if l.get("layout").get("row4").get("name") == objNameToRemove:
                                l.get("layout")["row4"] = {}

        # bpmnInstance.update(processObjs__set = [], form__set = [], forced=True)
        bpmnInstance.update(set__processObjs=processObjs, set__form=form)
        return Response({})
        #
        # updating = BpmnSerializer(instance=bpmnInstance, data={
        #     "processObjs": processObjs,
        #     "form": form}, partial=True)
        # updating.is_valid(raise_exception = True)
        # updating.save()


    """
        bpmnID: "5a5f41db2bb07d3ef421cff3"
        bpmnObjID: "UserTask_1w908k0"
    """


    @list_route(methods=["get"])
    def getTaskDetails(self, request, *args, **kwargs):
        bpmnInstance = Bpmn.objects.get(id=request.query_params.get("bpmnid"))
        taskName = request.query_params.get("objid")
        res = []
        xmlObj = ET.fromstring(bpmnInstance.xml)
        xmlObj = xpath_eval(xmlObj)
        for catch_event in xmlObj('.//bpmn:userTask'):
            res.append({'name': catch_event.get('name'), 'id': catch_event.get('id')})

        for form in bpmnInstance.form:
            if form.get('bpmnObjID') == taskName:
                title = ""
                for r in res:
                    if r.get("id") == taskName:
                        title = r.get("name")
                form["taskName"] = title
                # all = []
                # for _form in bpmnInstance.form:
                #     for field in _form["schema"]["fields"]:
                #         field["form"] = _form["bpmnObjID"]
                # all.append(field)
                # all = query(all).group_by(lambda x: x['name'],
                #                           result_selector=lambda key, group: {
                #                               "count":group.count(),
                #                               "displayName":group.first()['displayName'],
                #                               "type":group.first()['type'],
                #                               "name":group.first()['name'],
                #                           }).to_list()
                # for f in form["schema"]["fields"]:
                #     for a in all:
                #         if a["name"] == f["name"]:
                #             f["statics"] = a

                return Response(form)
        return Response({})


    def template_view(self, request, *args, **kwargs):
        return render_to_response('companyManagement/BPMN/datamodel.html', {},
                                  context_instance=RequestContext(request))
