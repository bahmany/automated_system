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
from amspApp.Bpms.models import LunchedProcess, LunchedProcessArchive, Statistic
from amspApp.Bpms.serializers.LunchedProcessArchiveSerializer import LunchedProcessArchiveSerializer
from amspApp.Bpms.serializers.LunchedProcessSerializer import LunchedProcessSerializer
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.FileServer.views.BpmsFileView import BpmsFileViewSet
from amspApp.amspUser.views.UserView import UserListPagination


class LunchedProcessViewSet(me_viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = LunchedProcess.objects.all()
    serializer_class = LunchedProcessSerializer
    pagination_class = UserListPagination
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)

    def get_queryset(self):
        return super(LunchedProcessViewSet, self).get_queryset()

    def retrieve(self, request, *args, **kwargs):
        result = super(LunchedProcessViewSet, self).retrieve(self, request, *args, **kwargs)
        if "formSchema" in result.data:
            if result.data["formSchema"]:
                for r in result.data["formSchema"]:
                    if "type" in r:
                        r["type"] = r["type"].replace("amf", "mrb")

        bpmnInstance = self.get_object()
        res = result.data["formSchema"]

        bpmnInstance.update(set__formSchema= res)
        return result


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # currentPosition = PositionsDocument.objects.get(userID=request.user.id,
            #                                                     companyID=request.user.current_company.id)
            #     try:
            #         counterObj = Statistic.objects.get(position_id=currentPosition.id)
            #     except:
            #         counterObj = Statistic(posotion_id=currentPosition.id)
            #     counterObj.Lp += 1
            #     counterObj.save()
            serializer.create(serializer.validated_data, request=request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({
                            'message': serializer.errors,
                            'status': 'Bad request',
                        }, status=status.HTTP_400_BAD_REQUEST)


    @list_route(methods=['post'])
    def getPoolResult(self, request, *args, **kwargs):
        pass


    @list_route(methods=['get'])
    def Inbox(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        item_per_page = request.GET.get('itemPerPage')

        if item_per_page and not item_per_page == 'undefined':
            self.pagination_class.page_size = item_per_page

        if query and not query == 'undefined':
            search_text = request.GET['query']
            queryset = LunchedProcess.objects.filter(Q(name__icontains=search_text))
        else:
            queryset = LunchedProcess.objects.all()
        posistionId = PositionsDocument.objects.get(userID=request.user.id, companyID=request.user.current_company.id)
        # try:
        #     counterObj = Statistic.objects.get(position_id=posistionId.id)
        # except:
        #     counterObj = Statistic(position_id=posistionId.id)
        #
        # counterObj.newLp = 0
        # counterObj.save()
        queryset = queryset.filter(thisPerformers__contains=str(posistionId.id))
        queryset = queryset.order_by('-postDate')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, fields=(
                'id', 'bpmnName', 'name', 'previousPerformer', 'postDate', 'lastInboxChangeDate', 'position_id'))
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, fields=(
            'id', 'bpmnName', 'name', 'previousPerformer', 'postDate', 'lastInboxChangeDate', 'position_id'))
        return Response(serializer.data)


    @detail_route(methods=['patch'])
    def CompleteJob(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        enginefileClass = BpmsFileViewSet()
        engineInstance = pickle.loads(enginefileClass.getEngineTempFile(instance.engineInstance))
        engineInstance.keep_going(request, instance.formData)
        posistionId = PositionsDocument.objects.get(userID=request.user.id, companyID=request.user.current_company.id)
        # try:
        #     counterObj = Statistic.objects.get(position_id=posistionId.id)
        # except:
        #     counterObj = Statistic(position_id=posistionId.id)
        #
        # counterObj.Lp -= 0
        # counterObj.save()
        return Response(serializer.data)


    @detail_route(methods=['patch'])
    def JustSaveIt(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


    def template_view_inbox(self, request, *args, **kwargs):
        gt_datas_title = [
            'bpmnName',
            'receivedFrom',
            'startProcess',
            'comeInInbox',
        ]

        gt_datas_dbtitle = [
            'bpmnName',
            'previousPerformer.profileName',
            'postDate',
            'lastInboxChangeDate',
        ]

        gt_buttons = [
            {'type': 'primary fa fa-gear', 'func': 'doJob(obj.id)', 'is_toggle_func': 's', 'is_toggle': 0},

        ]
        serializer = self.get_serializer()
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
                'gt_table_title': 'LunchedProcessInbox',
                'gt_object_name': 'LunchedProcess',
                'gt_func_col': 'col-md-1',
                'gt_search_func': 'searchLunchedProcess()',
                'gt_create_func': 'createLunchedProcess()',
                'gt_datas_title': gt_datas_title,
                'gt_datas_dbtitle': gt_datas_dbtitle,
                'gt_buttons': gt_buttons,
                'LunchedProcess_table_template': 'generic-templates/BpmsInboxTable.html',
                'LunchedProcess_edit_modal': 'generic-templates/Modal.html',
        }

        return render_to_response('Bpms/LunchedProcessInbox.html', data,
                                  context_instance=RequestContext(self.request))


    def template_view_do_process(self, request, *args, **kwargs):
        return render_to_response('Bpms/DoLunchedProcess.html', {},
                                  context_instance=RequestContext(request))

    def template_view_track_lunched_process(self, request, *args, **kwargs):
        return render_to_response('Bpms/TrackLunchedProcess.html', {},
                                  context_instance=RequestContext(request))

    def template_view_track_done_process(self, request, *args, **kwargs):
        return render_to_response('Bpms/TrackDoneProcess.html', {},
                                  context_instance=RequestContext(request))