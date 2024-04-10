import io
import pickle
from bson import ObjectId
from amspApp.BPMSystem.serializers.LPAInboxSerializer import LPAInboxSerializer
from amspApp.BPMSystem.serializers.LPInboxSerializer import LPInboxSerializer
from amspApp.BPMSystem.serializers.TrackLPASerializer import TrackLPASerializer
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
from amspApp.BPMSystem.models import LunchedProcess, LunchedProcessArchive, Statistic, BigArchive, \
    LunchedProcessMessages
from amspApp.BPMSystem.serializers.LunchedProcessArchiveSerializer import LunchedProcessArchiveSerializer
from amspApp.BPMSystem.serializers.LunchedProcessSerializer import LunchedProcessSerializer
from amspApp.BPMSystem.serializers.MessageProcessSerializer import MessageProcessSerializer
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.FileServer.views.BpmsFileView import BpmsFileViewSet
from amspApp.amspUser.views.UserView import UserListPagination


class LunchedProcessArchiveViewSet(me_viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = LunchedProcessArchive.objects.all()
    serializer_class = LunchedProcessArchiveSerializer
    pagination_class = UserListPagination
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)

    # def retrieve(self, request, *args, **kwargs):
    # instance = self.get_object()
    # serializer = self.get_serializer(instance,fields=('id', 'bpmnName',  'startProcessDate','name','realpastSteps'))
    # return Response(serializer.data)
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
    def SearchBar(self, request, *args, **kwargs):
        # query = self.request.GET.get('query')
        # item_per_page = request.GET.get('itemPerPage')
        posistionId = PositionsDocument.objects.get(userID=request.user.id, companyID=request.user.current_company.id)
        queryset = LunchedProcess.objects.filter(allPerformers__contains=str(posistionId.id), isHide=False)
        queryset = queryset.order_by('-postDate')
        res = {'starters': [], 'bpmns': []}
        whitUniqueBpmnId = queryset.distinct(field='bpmn.id')
        for itm in whitUniqueBpmnId:
            currnetList = queryset.filter(bpmn__id=itm)
            res['bpmns'].append({'name': currnetList[0].bpmn['name'], 'id': str(itm), 'count': currnetList.count()})
        whitUniquePosId = queryset.distinct(field='position_id')
        for itm in whitUniquePosId:
            currnetList = queryset.filter(position_id=itm)
            res['starters'].append({'name': currnetList[0].positionName, 'id': str(itm), 'count': currnetList.count(),
                                    'chartTitle': currnetList[0].chartTitle})
        return Response(res)

    # @list_route(methods=['get'])
    # def ListArchive(self, request, *args, **kwargs):
    # currPosition = PositionsDocument.objects.get(userID=request.user.id, companyID=request.user.current_company.id)
    #
    #     query = self.request.GET.get('query')
    #     item_per_page = request.GET.get('itemPerPage')
    #
    #     if item_per_page and not item_per_page == 'undefined':
    #         self.pagination_class.page_size = item_per_page
    #     posistionId = PositionsDocument.objects.get(userID=request.user.id, companyID=request.user.current_company.id)
    #     queryset = LunchedProcessArchive.objects.filter(performer=posistionId.id, isHide=False)
    #     # if request.query_params['isMine'] and request.query_params['isMine'] != 'undefined' and request.query_params[
    #     #     'isMine'] != '':
    #     #     if request.query_params['isMine'] == 'mine':
    #     #         queryset = queryset.filter(position_id=posistionId.id)
    #     #     elif request.query_params['isMine'] == 'notmine':
    #     #         queryset = queryset.filter(position_id__ne=posistionId.id)
    #
    #     # if query and not query == 'undefined':
    #     #     search_text = request.GET['query']
    #     #     queryset = queryset.filter((Q(name__icontains=search_text) | Q(positionName__icontains=search_text)))
    #     queryset = queryset.order_by('-postDate')
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer= LPAInboxSerializer(page, many=True, request=request, currentPositionObj=currPosition)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = LPAInboxSerializer(queryset, many=True, request=request, currentPositionObj=currPosition)
    #     return Response(serializer.data)


    @detail_route(methods=['get'])
    def LPATrack(self, request, *args, **kwargs):
        LPAid = kwargs['id']
        currPosition = PositionsDocument.objects.get(userID=request.user.id, companyID=request.user.current_company.id)
        instance = LunchedProcessArchive.objects.get(performer=currPosition.id, id=LPAid)
        serializer = TrackLPASerializer(instance=instance)
        return Response(serializer.data)


    @list_route(methods=['get'])
    def LunchedProcessArchive(self, request, *args, **kwargs):
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
        # posistionId = PositionsDocument.objects.get(userID=request.user.id, companyID=request.user.current_company.id)
        queryset = LunchedProcessArchive.objects.filter(performer=currPosition.id, isHide=False)

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
            serializer = LPAInboxSerializer(page, many=True, request=request, currentPositionObj=currPosition)
            return self.get_paginated_response(serializer.data)

        serializer = LPAInboxSerializer(queryset, many=True, request=request, currentPositionObj=currPosition)
        return Response(serializer.data)


    @detail_route(methods=['delete'])
    def HideLunchedProcess(self, request, *args, **kwargs):
        instance = LunchedProcessArchive.objects.get(id=ObjectId(kwargs['id']))
        instance.isHide = True
        instance.save()
        lpId=instance.lunchedProcessId
        itemForDelete = LunchedProcessMessages.objects.filter(lunchedProcessId=lpId)
        if itemForDelete.count() > 0:
            for _obj in itemForDelete:
                _obj.isHide = 1
                _obj.save()
        itemForDelete3 = BigArchive.objects.filter(processId=lpId)
        if itemForDelete3.count() > 0:
            for _obj in itemForDelete3:
                _obj.delete()
        itemForDelete2 = LunchedProcessArchive.objects.filter(lunchedProcessId=lpId)
        if itemForDelete2.count() > 0:
            for _obj in itemForDelete2:
                _obj.isHide = True
                _obj.formData['isDeleted'] = 1
                _obj.save()

                data = {
                    'user_id': instance.user_id,
                    'position_id': instance.position_id,
                    'positionName': instance.positionName,
                    'positionPic': instance.positionPic,
                    'bpmn': instance.bpmn,
                    'bpmnForCreate': "canceled",
                    'name': instance.name,
                    'thisStepName': 'فرایند حذف شد',
                    'thisPerformer': _obj.performer,
                    'pastSteps': instance.pastSteps,
                    'formData': _obj.formData,
                    'postDate': datetime.now(),
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
            lpForDelete=LunchedProcess.objects.get(id=lpId)
            lpForDelete.isHide=True
            lpForDelete.save()
        return Response(1)

    def template_view(self, request, *args, **kwargs):

        return render_to_response('Bpms/BaseLunchedProcessArchive.html', {},
                                  context_instance=RequestContext(self.request))
