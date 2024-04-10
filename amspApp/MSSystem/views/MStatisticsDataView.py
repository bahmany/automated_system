import io
import pickle

import timeago
from bson import ObjectId
from django.utils.timezone import UTC, pytz
from amspApp.BPMSystem.serializers.LPInboxSerializer import LPInboxSerializer
from amspApp.BPMSystem.serializers.ShowDiagramSerializer import ShowDiagramSerializer
from amspApp.BPMSystem.serializers.ShowFormSerializer import ShowFormSerializer
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionDocumentLessDataSerializer
from amspApp.Infrustructures.Classes.DateConvertors import convertTimeZoneToUTC, is_valid_shamsi_date, sh_to_mil, \
    mil_to_sh_with_time, PrettyDayShow, get_date_str
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
from amspApp.BPMSystem.models import LunchedProcess, LunchedProcessArchive, Statistic, BigArchive
from amspApp.BPMSystem.serializers.LunchedProcessSerializer import LunchedProcessSerializer
from amspApp.BPMSystem.serializers.MessageProcessSerializer import MessageProcessSerializer
from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.CompaniesManagment.Processes.serializers.BpmnSerializer import BpmnSerializer
from amspApp.FileServer.views.BpmsFileView import BpmsFileViewSet
from amspApp.Infrustructures.Classes import DateConvertors
from amspApp.MSSystem.models import MSData, MSTemplate
from amspApp.MSSystem.serializers.MSDataSerializer import MSDataInboxSerializer, MSDataSerializer
from amspApp.MSSystem.serializers.MSTemplateSerializer import MSTemplateSerializer
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.amspUser.views.UserView import UserListPagination
from pytz import timezone


class MStatisticsDataViewSet(me_viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = MSData.objects.all()
    serializer_class = MSDataInboxSerializer
    pagination_class = DetailsPagination
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)

    def create(self, request, *args, **kwargs):
        request.data['entryDate'] = convertTimeZoneToUTC(request.user.timezone, request.data['entryDate'])
        serializer = MSDataSerializer(data=request.data)
        if serializer.is_valid():
            posistionObj = PositionsDocument.objects.get(userID=request.user.id,
                                                         companyID=request.user.current_company.id)
            serializer.validated_data['position_id'] = posistionObj.id
            new = serializer.create(serializer.validated_data)
            return Response(str(new.pk), status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors,
                         'status': 'Bad request'},
                        status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        request.data['entryDate'] = convertTimeZoneToUTC(request.user.timezone, request.data['entryDate'])

        serializer = MSDataSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        item_per_page = request.GET.get('itemPerPage')
        tempId = request.GET.get('tempId')
        if item_per_page and not item_per_page == 'undefined':
            self.pagination_class.page_size = 50
        if query and not query == 'undefined':
            search_text = request.GET['query']
            queryset = MSData.objects.filter(
                Q(template_id=ObjectId(tempId)) & (Q(value__icontains=search_text) | Q(desc__icontains=search_text)))
        else:
            queryset = MSData.objects.filter(template_id=ObjectId(tempId))

        queryset = queryset.order_by('-id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def template_view_statistics_data(self, request, *args, **kwargs):
        return render_to_response('Statistics/DataStatisticTemplate.html', {},
                                  context_instance=RequestContext(request))

    @detail_route(methods=["get"])
    def getLastEntery(self, request, *args, **kwargs):
        last_instance = self.queryset.filter(template_id=kwargs.get('id')).order_by('-entryDate').first()
        last_date = last_instance.entryDate
        pretty = get_date_str(last_date)
        value = last_instance.value
        tml_id = MSTemplate.objects.get(id = last_instance.template_id)
        title = tml_id.name
        unit = tml_id.dataType
        position = PositionDocumentLessDataSerializer(instance=PositionsDocument.objects.get(id = last_instance.position_id)).data
        result = {
            'last_date': last_date,
            'value': value,
            'pretty': pretty,
            'last_date_pretty': timeago.format(last_date, datetime.now(), 'fa_IR'),
            'title':title,
            'unit':unit,
            'position':position,
        }
        return Response(result)

    @list_route(methods=["post"])
    def getData(self, request):
        tmplInstace = MSTemplate.objects.get(
            publishedUsersDetail__userID=request.user.id,
            id=request.data["tmplID"]
        )

        startDate = None
        endDate = None
        max = None
        min = None

        if 'startdate' in request.data:
            if is_valid_shamsi_date(request.data["startdate"]):
                dt = request.data["startdate"] + " 00:00:01"
                startDate = sh_to_mil(dt, has_time=True)

        if 'enddate' in request.data:
            if is_valid_shamsi_date(request.data["enddate"]):
                dt = request.data["enddate"] + " 23:59:59"
                endDate = sh_to_mil(dt, has_time=True)

        dataInstance = self.queryset.filter(template_id=tmplInstace.id).limit(50).order_by(request.data["order"])
        if startDate:
            dataInstance = dataInstance.filter(entryDate__gte=startDate)
        if endDate:
            dataInstance = dataInstance.filter(entryDate__lte=endDate)
        if max:
            dataInstance = dataInstance.filter(value__gte=max)
        if min:
            dataInstance = dataInstance.filter(value__lte=min)

        maxInstance = dataInstance.order_by("-value").limit(1)
        minInstance = dataInstance.order_by("value").limit(1)
        avgVal = int(dataInstance.average("value"))

        if maxInstance.count() == 0:
            maxInstance = None
        else:
            maxInstance = MSDataInboxSerializer(instance=maxInstance[0]).data
            maxInstance["entryDate"] = mil_to_sh_with_time(maxInstance["entryDate"])
            maxInstance["postDate"] = mil_to_sh_with_time(maxInstance["postDate"])
        if minInstance.count() == 0:
            minInstance = None
        else:
            minInstance = MSDataInboxSerializer(instance=minInstance[0]).data
            minInstance["entryDate"] = mil_to_sh_with_time(minInstance["entryDate"])
            minInstance["postDate"] = mil_to_sh_with_time(minInstance["postDate"])

        result = MSDataInboxSerializer(instance=dataInstance, many=True).data
        tmpl = MSTemplateSerializer(instance=tmplInstace).data

        for r in result:
            r["entryDate"] = mil_to_sh_with_time(r["entryDate"])
            r["postDate"] = mil_to_sh_with_time(r["postDate"]).split(".")[0]

        return Response({"dt": result, "tmpl": tmpl, "exp": {
            "max": maxInstance,
            "min": minInstance,
            "avg": avgVal
        }})
