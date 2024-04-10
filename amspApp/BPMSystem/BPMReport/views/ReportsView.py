import io
import json
import pickle
from bson import ObjectId
from django.http import HttpResponse
from amspApp.BPMSystem.BPMReport.models import ReportTemplate
from amspApp.BPMSystem.BPMReport.serializers.ReportDataSerializer import ReportDataSerializer
from amspApp.BPMSystem.BPMReport.serializers.ReportsSerializer import ReportTemplateSerializer
from amspApp.BPMSystem.BPMReport.utilities.GetExelFuncs import ReportToExel
from amspApp.BPMSystem.serializers.BigArchiveSerializer import BigArchiveSerializer
from amspApp.BPMSystem.serializers.LPInboxSerializer import LPInboxSerializer
from amspApp.BPMSystem.serializers.ShowDiagramSerializer import ShowDiagramSerializer
from amspApp.BPMSystem.serializers.ShowFormSerializer import ShowFormSerializer
from amspApp.CompaniesManagment.Charts.serializers.ChartSerializers import ChartSerializer
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh, sh_to_mil
from amspApp.Infrustructures.MySpiffWorkflow.bpmn.parser.util import xpath_eval
from datetime import datetime
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from mongoengine import Q
from rest_framework.decorators import detail_route, list_route
from rest_framework_mongoengine import viewsets as me_viewsets
from rest_framework.renderers import HTMLFormRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework import status
from amspApp.BPMSystem.MyEngine.BpmEngine import BpmEngine
from amspApp.BPMSystem.models import LunchedProcess, LunchedProcessArchive, Statistic, BigArchive, \
    ReportBpmnsPermissions, ReportData
from amspApp.BPMSystem.serializers.LunchedProcessSerializer import LunchedProcessSerializer
from amspApp.BPMSystem.serializers.MessageProcessSerializer import MessageProcessSerializer
from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.CompaniesManagment.Processes.serializers.BpmnSerializer import BpmnSerializer
from amspApp.FileServer.views.BpmsFileView import BpmsFileViewSet
from amspApp.MSSystem.models import MSTemplate, MSData
from amspApp.MSSystem.serializers.MSTemplateSerializer import MSTemplateSerializer, MSTemplateInboxSerializer
from amspApp._Share.GetMime import GetMimeType
from amspApp.amspUser.views.UserView import UserListPagination


class ReportsViewSet(me_viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = ReportTemplate.objects.all()
    serializer_class = ReportTemplateSerializer
    pagination_class = UserListPagination
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)

    @list_route(methods=['get'])
    def BmnsList(self, request, *args, **kwargs):
        posistionObj = PositionsDocument.objects.get(userID=request.user.id,
                                                     companyID=request.user.current_company.id)
        archiveRes = ReportBpmnsPermissions.objects.filter(chartId=posistionObj.chartID,
                                                           companyId=request.user.current_company.id)
        if archiveRes.count() == 1:
            return Response(archiveRes[0].bpmnsDetail)
        else:
            return Response([])

    @list_route(methods=['get'])
    def FieldsList(self, request, *args, **kwargs):
        posistionObj = PositionsDocument.objects.get(userID=request.user.id,
                                                     companyID=request.user.current_company.id)
        chartIds = ChartSerializer().get_list_chart_from_chartID(posistionObj.chartID)
        try:
            bpmnObj = Bpmn.objects.get(id=ObjectId(request.GET['bpmn']))
        except:
            return Response('ERROR')
        fieldsRes = BigArchive.objects.filter(thisPerformerChartId__in=chartIds,
                                              bpmnId=ObjectId(request.GET['bpmn'])).distinct(field='thisForm')
        finalRes = []
        for itm in bpmnObj.processObjs:
            if itm['name'] in fieldsRes:
                finalRes.append({'type': itm['type'], 'name': itm['name'], 'displayName': itm['displayName']})
        return Response(finalRes)

    @list_route(methods=['get'])
    def DataList(self, request, *args, **kwargs):
        posistionObj = PositionsDocument.objects.get(userID=request.user.id,
                                                     companyID=request.user.current_company.id)
        # chartIds = ChartSerializer().get_list_chart_from_chartID(posistionObj.chartID)

        resDataQuery = ReportData.objects.filter(chartId=posistionObj.chartID,
                                                 bpmnId=ObjectId(request.GET['bpmn']))

        if request.GET['starter'] and request.GET['starter'] != "undefined":
            resDataQuery = resDataQuery.filter(lpPositionName__icontains=request.GET['starter'])
        if request.GET['fromDate'] and request.GET['fromDate'] != "undefined":
            srchFromData = datetime.strptime(sh_to_mil(request.GET['fromDate']) + "T23:59:59",
                                             "%Y/%m/%dT%H:%M:%S")
            resDataQuery = resDataQuery.filter(lpStartDate__gte=srchFromData)
        if request.GET['toDate'] and request.GET['toDate'] != "undefined":
            srchToData = datetime.strptime(sh_to_mil(request.GET['toDate']) + "T23:59:59",
                                           "%Y/%m/%dT%H:%M:%S")
            resDataQuery = resDataQuery.filter(lpStartDate__lte=srchToData)
        if request.GET['isDone'] and request.GET['isDone'] != "undefined":
            if request.GET['isDone'] == '1':
                resDataQuery = resDataQuery.filter(isDone=True)
            elif request.GET['isDone'] == '0':
                resDataQuery = resDataQuery.filter(isDone=False)

        page = self.paginate_queryset(resDataQuery)
        fieldsList = json.loads(request.GET['fields'])
        if page is not None:
            serializer = ReportDataSerializer(page, many=True, dataFields=fieldsList)
            return self.get_paginated_response(serializer.data)

        serializer = ReportDataSerializer(resDataQuery, many=True, dataFields=fieldsList)
        return Response(serializer.data)


    @list_route(methods=['get'])
    def XLSDataFile(self, request, *args, **kwargs):
        posistionObj = PositionsDocument.objects.get(userID=request.user.id,
                                                     companyID=request.user.current_company.id)

        resDataQuery = ReportData.objects.filter(chartId=posistionObj.chartID,
                                                 bpmnId=ObjectId(request.GET['bpmn']))

        if request.GET['starter'] and request.GET['starter'] != "undefined":
            resDataQuery = resDataQuery.filter(lpPositionName__icontains=request.GET['starter'])
        if request.GET['fromDate'] and request.GET['fromDate'] != "undefined":
            srchFromData = datetime.strptime(sh_to_mil(request.GET['fromDate']) + "T23:59:59",
                                             "%Y/%m/%dT%H:%M:%S")
            resDataQuery = resDataQuery.filter(lpStartDate__gte=srchFromData)
        if request.GET['toDate'] and request.GET['toDate'] != "undefined":
            srchToData = datetime.strptime(sh_to_mil(request.GET['toDate']) + "T23:59:59",
                                           "%Y/%m/%dT%H:%M:%S")
            resDataQuery = resDataQuery.filter(lpStartDate__lte=srchToData)
        if request.GET['isDone'] and request.GET['isDone'] != "undefined":
            if request.GET['isDone'] == '1':
                resDataQuery = resDataQuery.filter(isDone=True)
            elif request.GET['isDone'] == '0':
                resDataQuery = resDataQuery.filter(isDone=False)
        fieldsList = json.loads(request.GET['fields'])
        fieldsIds = json.loads(request.GET['fieldsIds'])
        serializer = ReportDataSerializer(resDataQuery, many=True, dataFields=fieldsIds)
        XLSfile = ReportToExel(serializer.data, fieldsList, fieldsIds)
        # reading file into memory---
        # reading file into memory---
        f = XLSfile
        fsock = open(f, "rb")
        # mime = GetMimeType(f.split(".")[1])
        response = HttpResponse(fsock, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s' % (f.split('/')[-1])
        return response

    @detail_route(methods=["get"])
    def getBigArchiveHistory(self, request, *args, **kwargs):
        all = BigArchive.objects.filter(processId = kwargs["id"], isStepDone = True).order_by("-id")
        all = BigArchiveSerializer(instance=all, many=True).data
        return Response(all)


    @list_route(methods=["get"])
    def SearchID(self, request):
        results = {
            "ok": "not found",
            "results": []
        }
        toSearch = request.query_params["q"]
        if toSearch == "":
            return Response(results)
        if len(toSearch) != 24:
            return Response(results)

        bigArcInstance = BigArchive.objects.filter(id = toSearch).first()

        if bigArcInstance:
            archs = BigArchive.objects.filter(processId = bigArcInstance.processId).order_by("-id")
            results = BigArchiveSerializer(instance=archs, many=True).data
            for r in results:
                if toSearch == r["id"]:
                    r["thisis"] = True
            results = {
                "results": results,
                "ok":"ok"
            }
        return Response(results)



    def template_view_reports_base(self, request, *args, **kwargs):
        return render_to_response('Bpms/ProcessReports.html', {},
                                  context_instance=RequestContext(request))


    def template_view_search_base(self, request, *args, **kwargs):
        return render_to_response('Bpms/ProcessSearch.html', {},
                                  context_instance=RequestContext(request))
