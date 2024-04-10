import io
import pickle
from amspApp.BPMSystem.serializers.DPAInboxSerializer import DPAInboxSerializer
from amspApp.BPMSystem.serializers.DPAShowDataSerializer import DPAShowDataSerializer
from amspApp.BPMSystem.serializers.TrackDPASerializer import TrackDPASerializer
from amspApp.Infrustructures.MySpiffWorkflow.bpmn.parser.util import xpath_eval
from datetime import datetime
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from mongoengine import Q
from rest_framework.decorators import detail_route, list_route

from rest_framework_mongoengine import viewsets as me_viewsets
from rest_framework.renderers import HTMLFormRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
import xml.etree.ElementTree as ET

from rest_framework import status
from amspApp.BPMSystem.models import LunchedProcess, LunchedProcessArchive, DoneProcessArchive, Statistic
from amspApp.BPMSystem.serializers.DoneProcessArchiveSerializer import DoneProcessArchiveSerializer
from amspApp.BPMSystem.serializers.LunchedProcessSerializer import LunchedProcessSerializer
from amspApp.BPMSystem.serializers.MessageProcessSerializer import MessageProcessSerializer
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.FileServer.views.BpmsFileView import BpmsFileViewSet
from amspApp.amspUser.views.UserView import UserListPagination


class DoneProcessArchiveViewSet(me_viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = DoneProcessArchive.objects.all()
    serializer_class = DoneProcessArchiveSerializer
    pagination_class = UserListPagination
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.create(serializer.validated_data, request=request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({
                            'message': serializer.errors,
                            'status': 'Bad request',
                        }, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'])
    def DoneProcessArchive(self, request, *args, **kwargs):
        currPosition = PositionsDocument.objects.get(userID=request.user.id, companyID=request.user.current_company.id)
        query = {}
        query['bpmn'] = self.request.GET.get('bpmn')
        query['name'] = self.request.GET.get('name')
        query['receive'] = self.request.GET.get('receive')
        query['starter'] = self.request.GET.get('starter')
        query['fromDate'] = self.request.GET.get('fromDate')
        query['toDate'] = self.request.GET.get('toDate')

        item_per_page = request.GET.get('itemPerPage')

        if item_per_page and not item_per_page == 'undefined':
            self.pagination_class.page_size = item_per_page
        queryset = DoneProcessArchive.objects.filter(performer=currPosition.id, isHide=False)

        if not query['bpmn'] == 'undefined':
            queryset = queryset.filter(bpmnName__icontains=query['bpmn'])
        if not query['name'] == 'undefined':
            queryset = queryset.filter(name__icontains=query['name'])
        if not query['receive'] == 'undefined':
            queryset = queryset.filter(lastUrPrevPerformerName__icontains=query['receive'])
        if not query['starter'] == 'undefined':
            queryset = queryset.filter(positionName__icontains=query['starter'])
        # if not query['fromDate'] == 'undefined':
        #     queryset = queryset.filter(fromDate__icontains=query['fromDate'])
        # if not query['toDate'] == 'undefined':
        #     queryset = queryset.filter(toDate__icontains=query['toDate'])
        queryset = queryset.order_by('-postDate')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = DPAInboxSerializer(page, many=True, request=request, currentPositionObj=currPosition)
            return self.get_paginated_response(serializer.data)

        serializer = DPAInboxSerializer(queryset, many=True, request=request, currentPositionObj=currPosition)
        return Response(serializer.data)


    @detail_route(methods=['get'])
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DPAShowDataSerializer(instance)
        return Response(serializer.data)

    @detail_route(methods=['delete'])
    def HideLunchedProcess(self, request, *args, **kwargs):
        instance = self.get_object()
        itemForDelete = DoneProcessArchive.objects.filter(lunchedProcessId=instance.id)
        if itemForDelete.count() > 0:
            for _obj in itemForDelete:
                _obj.isHide = 1
                _obj.save()
                _obj.formData['isDeleted'] = 1
                data = {
                    'user_id': _obj.user_id,
                    'position_id': _obj.position_id,
                    'positionName': _obj.positionName,
                    'bpmn': _obj.bpmn,
                    'bpmnForCreate': _obj.bpmnForCreate,
                    'name': _obj.name,
                    'thisStep': _obj.steps[0],
                    'thisPerformer': _obj.performer,
                    'pastSteps': instance.pastSteps,
                    'engineInstance': _obj.engineInstance,
                    'formData': _obj.formData,
                    'postDate': _obj.postDate,
                    'lastInboxChangeDate': datetime.now()
                }
                serializer = MessageProcessSerializer(data=data)
                if serializer.is_valid():
                    serializer.create(serializer.validated_data)
                    # try:
                    #     counterObj = Statistic.objects.get(position_id=_obj.performer)
                    # except:
                    #     counterObj = Statistic(position_id=_obj.performer)
                    # counterObj.Mp += 1
                    # counterObj.newMp += 1
                    # counterObj.save()
        serializer = self.get_serializer(instance, data={'isHide': True}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(1)



    def template_view(self, request, *args, **kwargs):


        return render_to_response('Bpms/BaseDoneProcessArchive.html', {},
                                  context_instance=RequestContext(self.request))


    @detail_route(methods=['get'])
    def DPATrack(self, request, *args, **kwargs):
        DPAid = kwargs['id']
        currPosition = PositionsDocument.objects.get(userID=request.user.id, companyID=request.user.current_company.id)
        instance = DoneProcessArchive.objects.get(performer=currPosition.id, id=DPAid)
        serializer = TrackDPASerializer(instance=instance)
        return Response(serializer.data)