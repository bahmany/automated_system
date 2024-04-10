import io
import pickle
from django.core.cache import cache
from amspApp.BPMSystem.serializers.MPInboxSerializer import MPInboxSerializer
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
from amspApp.BPMSystem.models import LunchedProcess, LunchedProcessArchive, LunchedProcessMessages, Statistic
from amspApp.BPMSystem.serializers.LunchedProcessArchiveSerializer import LunchedProcessArchiveSerializer
from amspApp.BPMSystem.serializers.LunchedProcessSerializer import LunchedProcessSerializer
from amspApp.BPMSystem.serializers.MessageProcessSerializer import MessageProcessSerializer
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.FileServer.views.BpmsFileView import BpmsFileViewSet
from amspApp.Notifications.models import Notifications
from amspApp.Notifications.views.NotificationView import NotificationViewSet
from amspApp.amspUser.views.UserView import UserListPagination


class MessageProcessViewSet(me_viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = LunchedProcessMessages.objects.all()
    serializer_class = MessageProcessSerializer
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.seen=True
        instance.save()
        # =============================================Notification========
        Notifications.objects.filter(
            userID=request.user.id, type=3,
            extra__url='/dashboard/Process/Message/' + str(instance.id) + '/DoMessage'
        ).delete()

        NotificationViewSet().changesHappened(request.user.id)
        # cache.set(str(request.user.id) + "TopNotification", None)
        # cache.set(str(request.user.id) + "hasNotification", True)
        # =============================================Notification========
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    @list_route(methods=['get'])
    def Inbox(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        item_per_page = request.GET.get('itemPerPage')

        if item_per_page and not item_per_page == 'undefined':
            self.pagination_class.page_size = item_per_page

        if query and not query == 'undefined':
            search_text = request.GET['query']
            queryset = LunchedProcessMessages.objects.filter(Q(name__icontains=search_text))
        else:
            queryset = LunchedProcessMessages.objects.all()
        posistionId = PositionsDocument.objects.get(userID=request.user.id, companyID=request.user.current_company.id)
        # try:
        #     counterObj = Statistic.objects.get(position_id=posistionId.id)
        # except:
        #     counterObj = Statistic(position_id=posistionId.id)
        #
        # counterObj.newMp = 0
        # counterObj.save()
        queryset = queryset.filter(thisPerformer=str(posistionId.id))
        queryset = queryset.order_by('-postDate')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MPInboxSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = MPInboxSerializer(page, many=True)

        return Response(serializer.data)


    @detail_route(methods=['patch'])
    def SeenMessage(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # posistionId = PositionsDocument.objects.get(userID=request.user.id, companyID=request.user.current_company.id)
        # try:
        #     counterObj = Statistic.objects.get(position_id=posistionId.id)
        # except:
        #     counterObj = Statistic(position_id=posistionId.id)
        #
        # counterObj.Mp -= 0
        return Response(serializer.data)


    def template_view_message_process(self, request, *args, **kwargs):
        gt_datas_title = [
            'bpmnName',
            'startProcess',
        ]

        gt_datas_dbtitle = [
            'bpmnName',
        ]

        gt_buttons = [
            {'type': 'primary fa fa-search', 'func': 'retrieveMessageProcess(obj.id)', 'is_toggle_func': 's',
             'is_toggle': 0},

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
                                 'gm_modal_title': 'MessageLunchedProcess',
                                 'gm_modal_id': 'GenericModalTaskCreate.html',
                                 'gm_form': gm_task_create_form,
                                 'gm_buttons': gm_task_create_buttons}],
                'gt_table_title': 'MessageProcessArchive',
                'gt_object_name': 'MessageProcess',
                'gt_func_col': 'col-md-1',
                'gt_search_func': 'searchMessageProcess()',
                'gt_create_func': 'createLunchedProcess()',
                'gt_datas_title': gt_datas_title,
                'gt_datas_dbtitle': gt_datas_dbtitle,
                'gt_buttons': gt_buttons,
                'MessageProcess_table_template': 'generic-templates/MessageProcessTable.html',
                'MessageProcess_edit_modal': 'generic-templates/Modal.html',
        }

        return render_to_response('Bpms/BaseMessageProcessInbox.html', data,
                                  context_instance=RequestContext(request))


    def template_view_do_message_process(self, request, *args, **kwargs):

        return render_to_response('Bpms/DoMessageProcess.html', {},
                                  context_instance=RequestContext(request))
