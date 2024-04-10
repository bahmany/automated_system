import io
import pickle
from amspApp.Infrustructures.MySpiffWorkflow.bpmn.parser.util import xpath_eval
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from mongoengine import Q
from rest_framework.decorators import detail_route, list_route

from rest_framework_mongoengine import viewsets as me_viewsets
from rest_framework.renderers import HTMLFormRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
import xml.etree.ElementTree as ET

from rest_framework import status
from amspApp.Bpms.models import LunchedProcess, LunchedProcessArchive, DoneProcessArchive
from amspApp.Bpms.serializers.DoneProcessArchiveSerializer import DoneProcessArchiveSerializer
from amspApp.Bpms.serializers.LunchedProcessSerializer import LunchedProcessSerializer
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.FileServer.views.BpmsFileView import BpmsFileViewSet
from amspApp.amspUser.views.UserView import UserListPagination


class DoneProcessArchiveViewSet(me_viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = DoneProcessArchive.objects.all()
    serializer_class = DoneProcessArchiveSerializer
    pagination_class = UserListPagination
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)

    def get_queryset(self):
        return super(DoneProcessArchiveViewSet, self).get_queryset()

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
        posistionId = PositionsDocument.objects.get(userID=request.user.id, companyID=request.user.current_company.id)
        queryset = DoneProcessArchive.objects.filter(performer=str(posistionId.id))
        if request.query_params['isMine'] and request.query_params['isMine'] != 'undefined':
            if request.query_params['isMine'] == 'mine':
                queryset = queryset.filter(position_id=posistionId.id)
            elif request.query_params['isMine'] == 'notmine':
                queryset = queryset.filter(position_id__ne=posistionId.id)

        queryset = queryset.order_by('-postDate')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True,
                                             fields=('id', 'bpmnName', 'startProcessDate', 'name', 'postDate'))
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True,
                                         fields=('id', 'bpmnName', 'startProcessDate', 'name', 'postDate'))
        return Response(serializer.data)

    def template_view(self, request, *args, **kwargs):
        gt_datas_title = [
            'bpmnName',
            'startProcess',
            'endProcess',
        ]

        gt_datas_dbtitle = [
            'bpmnName',
        ]

        gt_buttons = [
            {'type': 'primary fa fa-search', 'func': 'reviewMyProcess(obj.id)', 'is_toggle_func': 's', 'is_toggle': 0},
        ]
        serializer = LunchedProcessSerializer()
        renderer = HTMLFormRenderer()
        gm_task_create_form = renderer.render(serializer.data, renderer_context={
            'template': 'forms/LunchedProcess/CreateLunchedProcess.html',
            'request': self.request
        })
        # ali = render(request, 'forms/task/CreateTask.html',{})
        gm_task_create_buttons = [
            {'type': 'primary fa fa-save', 'func': 'saveLunchedProcess()', 'title': ''},
            {'type': 'danger fa fa-times', 'func': 'cancel()', 'title': ''},
        ]
        # gt_ means GenericTable
        # gm_ means GenericModal

        data = {'gm_items': [{
            'gm_modal_title': 'createLunchedProcess',
            'gm_modal_id': 'GenericModalTaskCreate.html',
            'gm_form': gm_task_create_form,
            'gm_buttons': gm_task_create_buttons}],
            'gt_table_title': 'DoneProcessArchive',
            'gt_object_name': 'LunchedProcess',
            'gt_func_col': 'col-md-1',
            'gt_search_func': 'searchLunchedProcess()',
            'gt_create_func': 'createLunchedProcess()',
            'gt_datas_title': gt_datas_title,
            'gt_datas_dbtitle': gt_datas_dbtitle,
            'gt_buttons': gt_buttons,
            'LunchedProcess_table_template': 'generic-templates/DoneProcessArchiveTable.html',
            'LunchedProcess_edit_modal': 'generic-templates/Modal.html',
        }

        return render_to_response('Bpms/DoneProcessArchive.html', data, context_instance=RequestContext(self.request))
