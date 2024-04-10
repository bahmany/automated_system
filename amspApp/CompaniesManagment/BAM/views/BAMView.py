import io
from datetime import datetime, timedelta
from bson import ObjectId
from django.shortcuts import render_to_response
from django.template import RequestContext
from mongoengine import Q
from rest_framework.decorators import list_route, detail_route, permission_classes as _pc
from rest_framework.permissions import IsAuthenticated
from rest_framework_mongoengine import viewsets as me_viewsets
from rest_framework.renderers import HTMLFormRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
import xml.etree.ElementTree as ET

from rest_framework import status
from amspApp.BPMSystem.models import BigArchive, LunchedProcess
from amspApp.CompaniesManagment.BAM.models import Shakhes
from amspApp.CompaniesManagment.BAM.serializers.BAMSerializer import BAMSerializer, ShakhesSerializer, \
    ShakhesInboxSerializer
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.CompaniesManagment.Processes.serializers.BpmnSerializer import BpmnSerializer
from amspApp.CompaniesManagment.Processes.validators.BPMNValidator import BPMNValidator
from amspApp.CompaniesManagment.permissions.CompanyPermissions import CanCruid, IsOwnerOrReadOnly
from amspApp.CompaniesManagment.permissions.PermissionChecker import get_permissions
from amspApp.Infrustructures.MySpiffWorkflow.bpmn.parser.util import xpath_eval
from amspApp.amspUser.views.UserView import UserListPagination


class BAMViewSet(me_viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = BigArchive.objects.all()
    serializer_class = BAMSerializer
    pagination_class = UserListPagination
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)
    # permission_name = "Can_edit_BAM"
    # permission_classes = (CanCruid,)

    # def get_permissions(self):
    # return get_permissions(self, BAMViewSet)
    def getMonitorRes(self, shakhesObj, qry):
        isDone = True
        if shakhesObj.done_or_run:
            isDone = False
        monitorQry = qry
        if not shakhesObj.is_all_steps:
            monitorQry = monitorQry.filter(taskId=shakhesObj.step_id, isStepDone=isDone).count()
        else:
            monitorQry = monitorQry.filter(isProcessDone=isDone).distinct(field='processId')
            monitorQry = len(monitorQry)
        monitrStatus = 0
        if monitorQry < shakhesObj.min_mess:
            monitrStatus = 1
        if monitorQry >= shakhesObj.min_mess and monitorQry <= shakhesObj.start_warn:
            monitrStatus = 0
        if monitorQry >= shakhesObj.start_warn and monitorQry <= shakhesObj.start_danger:
            monitrStatus = 2
        if monitorQry >= shakhesObj.start_danger:
            monitrStatus = 3

        monitorRes = {
            'count': monitorQry,
            'min': shakhesObj.min_mess,
            'warn': shakhesObj.start_warn,
            'danger': shakhesObj.start_danger,
            'days': shakhesObj.time_period,
            'status': monitrStatus
        }
        return monitorRes

    def destroy(self, request, *args, **kwargs):
        instance = Shakhes.objects.get(id=self.kwargs["id"])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        postData = request.data
        posistionObj = PositionsDocument.objects.get(userID=request.user.id,
                                                     companyID=request.user.current_company.id)

        postData['user_id'] = int(request.user.id)
        postData['company_id'] = int(request.user.current_company.id)
        postData['position_id'] = posistionObj.id
        postData['position_name'] = posistionObj.profileName
        if 'bpmn_id' in postData and postData['bpmn_id']:
            postData['bpmn_id'] = ObjectId(postData['bpmn_id'])
        else:
            return Response({'bpmn_id': 'required'}, status=status.HTTP_400_BAD_REQUEST)
        if 'step_id' in postData and postData['step_id'] == 0:
            postData['is_all_steps'] = 1
        else:
            postData['is_all_steps'] = 0
        serializer = ShakhesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        compId = int(self.kwargs["companyID_id"])
        queryset = Shakhes.objects.filter(company_id=compId)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ShakhesInboxSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ShakhesInboxSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = Shakhes.objects.get(id=self.kwargs['id'])
        serializer = ShakhesSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        postData = request.data
        posistionObj = PositionsDocument.objects.get(userID=request.user.id,
                                                     companyID=request.user.current_company.id)

        postData['user_id'] = int(request.user.id)
        postData['company_id'] = int(request.user.current_company.id)
        postData['position_id'] = posistionObj.id
        postData['position_name'] = posistionObj.profileName
        if not 'extra' in postData:
            postData['extra'] = {}
        elif not postData['extra']:
            postData['extra'] = {}
        if 'bpmn_id' in postData and postData['bpmn_id']:
            postData['bpmn_id'] = ObjectId(postData['bpmn_id'])
        else:
            return Response({'bpmn_id': 'required'}, status=status.HTTP_400_BAD_REQUEST)
        if 'step_id' in postData and postData['step_id'] == 0:
            postData['is_all_steps'] = 1
        else:
            postData['is_all_steps'] = 0
        serializer = ShakhesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @list_route(methods=['get'])
    def AllRunningReport(self, request, *args, **kwargs):
        compId = int(self.kwargs["companyID_id"])
        runningProcessIds = BigArchive.objects.filter(isProcessDone=False, isStepDone=False)
        bpmnList = Bpmn.objects.filter(company_id=compId)
        reportRes = []
        totalrunning = 0
        for itm in bpmnList:
            thisCount = len(runningProcessIds.filter(bpmnId=itm.id).distinct(field='processId'))
            if thisCount > 0:
                reportRes.append({"name": itm.name, "value": thisCount})
                totalrunning += thisCount

        return Response({'report': reportRes, 'totalRunning': totalrunning})

    @list_route(methods=['get'])
    def AllDoneReport(self, request, *args, **kwargs):
        compId = int(self.kwargs["companyID_id"])
        doneProcessIds = BigArchive.objects.filter(isProcessDone=True)
        bpmnList = Bpmn.objects.filter(company_id=compId)
        reportRes = []
        totalrunning = 0
        for itm in bpmnList:
            thisCount = len(doneProcessIds.filter(bpmnId=itm.id).distinct(field='processId'))
            if thisCount > 0:
                reportRes.append({"name": itm.name, "value": thisCount})
                totalrunning += thisCount

        return Response({'report': reportRes, 'totalDone': totalrunning})

    @detail_route(methods=['get'])
    def ShakhesReport(self, request, *args, **kwargs):
        # compId = int(self.kwargs["companyID_id"])
        shakhesId = self.kwargs["id"]
        shakhesObj = Shakhes.objects.filter(id=ObjectId(shakhesId))[0]
        qry = BigArchive.objects.all()
        qry = qry.filter(bpmnId=shakhesObj.bpmn_id)
        if shakhesObj.time_period != 0:
            qry = qry.filter(postDate__gte=datetime.now() - timedelta(days=shakhesObj.time_period))
        qryRunn = qry.filter(isProcessDone=False)
        qryDone = qry.filter(isProcessDone=True)
        totalRun = len(qryRunn.distinct(field='processId'))
        totalDone = len(qryDone.distinct(field='processId'))
        monitorRes = self.getMonitorRes(shakhesObj, qry)
        qryRunn = qryRunn.filter(isStepDone=False).aggregate(
            {
                '$group': {
                    '_id': "$taskId",
                    'name': {"$first": "$taskName"}, 'processIds': {"$push": "$processId"}}

            })
        repRunn = []
        for itm in qryRunn:
            repRunn.append({'name': itm['name'], 'value': int(len(itm['processIds']))})

        qryDone = qryDone.filter(isStepDone=True).aggregate(
            {
                '$group': {'_id': "$taskId", 'name': {"$first": "$taskName"}, 'processIds': {"$push": "$processId"}}
            })
        repDone = []
        for itm in qryDone:
            repDone.append({'name': itm['name'], 'value': int(len(itm['processIds']))})
        return Response(
            {'monitorRes': monitorRes, 'repRunning': repRunn, 'repDone': repDone, 'totalDone': totalDone,
             'totalRunning': totalRun, 'bpmn_name': shakhesObj.bpmn_name, 'name': shakhesObj.name})

    @list_route(methods=['get'])
    def GetBpmns(self, request, *args, **kwargs):
        compId = int(self.kwargs["companyID_id"])
        bpmnList = Bpmn.objects.filter(company_id=compId)
        res = []
        totalrunning = 0
        for itm in bpmnList:
            res.append({"name": itm.name, "id": str(itm.id)})

        return Response(res)

    @detail_route(methods=['get'])
    def GetSteps(self, request, *args, **kwargs):
        bpmnId = self.kwargs["id"]
        bpmnObj = Bpmn.objects.filter(id=ObjectId(bpmnId))[0]
        res = []
        usrTsks = bpmnObj.userTasks
        xmlObj = ET.fromstring(bpmnObj.xml)
        xmlObj = xpath_eval(xmlObj)
        for catch_event in xmlObj('.//bpmn:userTask'):
            res.append({'name': catch_event.get('name'), 'id': catch_event.get('id')})

        return Response(res)

    #
    #
    def template_view(self, request, *args, **kwargs):
        return render_to_response('companyManagement/BAMbase.html', {},
                                  context_instance=RequestContext(self.request))


    def template_view_dashboard(self, request, *args, **kwargs):
        return render_to_response('companyManagement/BAMDashboard.html', {},
                                  context_instance=RequestContext(self.request))


    def template_view_new(self, request, *args, **kwargs):
        return render_to_response('companyManagement/BAMNew.html', {},
                                  context_instance=RequestContext(self.request))


    def template_view_shakhes(self, request, *args, **kwargs):
        return render_to_response('companyManagement/BAMShakhesReport.html', {},
                                  context_instance=RequestContext(self.request))


    def template_view_shakhes_edit(self, request, *args, **kwargs):
        return render_to_response('companyManagement/BAMEdit.html', {},
                                  context_instance=RequestContext(self.request))



