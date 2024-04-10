import pickle
from datetime import datetime
from urllib.parse import urlencode

from django.shortcuts import render_to_response
from django.template import RequestContext
from mongoengine import Q
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.renderers import HTMLFormRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets as me_viewsets

from amspApp.BPMSystem.MyEngine.BpmEngine import BpmEngine
from amspApp.BPMSystem.MyEngine.UserScriptTaskLuncher import UserTaskScriptLauncher
from amspApp.BPMSystem.models import LunchedProcess, LunchedProcessArchive, BigArchive, SqlTableSelectedItems, \
    ExtraSqlDataForTableSelectedItems
from amspApp.BPMSystem.serializers.LPInboxSerializer import LPInboxSerializer
from amspApp.BPMSystem.serializers.LunchedProcessSerializer import LunchedProcessSerializer
from amspApp.BPMSystem.serializers.MessageProcessSerializer import MessageProcessSerializer
from amspApp.BPMSystem.serializers.ShowDiagramSerializer import ShowDiagramSerializer
from amspApp.BPMSystem.serializers.ShowFormSerializer import ShowFormSerializer
from amspApp.CompaniesManagment.Connections.models import ConnectionPools, Connections
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsPoolViews import ConnectionPoolsViewSet
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.FileServer.views.BpmsFileView import BpmsFileViewSet
from amspApp.Notifications.models import Notifications
from amspApp.Notifications.views.NotificationView import NotificationViewSet
from amspApp.amspUser.views.UserView import UserListPagination


class LunchedProcessViewSet(me_viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = LunchedProcess.objects.all()
    serializer_class = LunchedProcessSerializer
    pagination_class = UserListPagination
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)

    def retrieve(self, request, *args, **kwargs):
        insObj = kwargs.get("id")
        instance = self.queryset.get(id=insObj)
        # instance = self.get_object()
        seenDates = instance.seen
        curPos = PositionsDocument.objects.get(userID=request.user.id, companyID=request.user.current_company.id)
        for itm in seenDates:
            if str(curPos.id) in itm.keys():
                itm[str(curPos.id)] = datetime.now()
                break
        instance.seen = seenDates
        instance.save()
        # =============================================Notification========
        Notifications.objects.filter(
            userID=request.user.id, type=2,
            extra__url='/dashboard/Process/Inbox/' + str(instance.id) + '/Do'
        ).delete()

        NotificationViewSet().changesHappened(request.user.id)
        # cache.set(str(request.user.id) + "TopNotification", None)
        # cache.set(str(request.user.id) + "hasNotification", True)
        # =============================================Notification========
        serializer = ShowFormSerializer(instance, request=request, currentPositionObj=curPos)
        dt = serializer.data
        dt["storage"] = instance.bpmn.get('storage')
        result = Response(dt)

        # if "formSchema" in result.data:
        #     if result.data["formSchema"]:
        #         if "fields" in result.data["formSchema"]:
        #             if result.data["formSchema"]["fields"]:
        #                 for r in result.data["formSchema"]["fields"]:
        #                     if "type" in r:
        #                         r["type"] = r["type"].replace("amf", "mrb")
        #
        # bpmnInstance = self.get_object()
        # res = result.data["formSchema"]

        # bpmnInstance.update(set__formSchema= res)

        return result

    @detail_route(methods=['get'])
    def Diagram(self, request, *args, **kwargs):
        instance = self.get_object()
        curPos = PositionsDocument.objects.get(userID=request.user.id, companyID=request.user.current_company.id)
        serializer = ShowDiagramSerializer(instance, request=request, currentPositionObj=curPos)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new = serializer.create(serializer.validated_data, request=request)
            engineInstance = BpmEngine(new)
            enginefileClass = BpmsFileViewSet()
            # new = self.handleAdvanceTables(new)
            enginefileClass = enginefileClass.createEngineTempFile(pickle.dumps(engineInstance))
            new.engineInstance = enginefileClass
            new.save()
            engineInstance.run(request)
            result = serializer.data
            # mohammad reza : 940825
            # added result["id"] to after create response because of showing created process form after pressing new btn
            result["id"] = str(new.id)
            # ------------------------------
            return Response(result, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors,
                         'status': 'Bad request'},
                        status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['post'])
    def getPoolResult(self, request, *args, **kwargs):
        schema = request.DATA['field']
        value = request.DATA['value']
        connection = Connections.objects.get(id=schema["connection"])
        pool = ConnectionPools.objects.get(id=schema["pool"])
        result = ConnectionPoolsViewSet().runCode(connection, pool, value)
        return Response(result)

    @list_route(methods=['get'])
    def getTablePoolResult(self, request, *args, **kwargs):
        # getting required instances
        connectionInstance = Connections.objects.get(id=request.query_params.get("conid"))
        connectionPoolInstance = ConnectionPools.objects.get(id=request.query_params.get("plid"))
        ProcessInstance = LunchedProcess.objects.get(id=request.query_params.get("currentProc"))
        taskname = request.query_params.get("tskname")
        taskId = request.query_params.get("taskID")

        if not ProcessInstance:  # if process completed
            ProcessInstance = LunchedProcessArchive.objects.filter(id=request.query_params.get("processid")).first()

        # finding and linking process form field to database
        currentTaskDict = {}
        for task in ProcessInstance.bpmn['form']:
            if task["bpmnObjID"] == taskId:
                for field in task["schema"]["fields"]:
                    if field.get("name") == taskname:
                        currentTaskDict = field

        values = {
            'offsetcount': int(request.query_params.get("offsetcount")),
            'nextcount': int(request.query_params.get("nextcount")),
            'searchFieldName': request.query_params.get("searchFieldName"),
            'searchText': request.query_params.get("searchText"),
        }

        result = ConnectionPoolsViewSet().run(connectionInstance, connectionPoolInstance, values)
        result["cols"] = list(result["cols"])

        selected = SqlTableSelectedItems.objects.filter(
            connectionPoolID=str(connectionPoolInstance.id),
            process=str(ProcessInstance.id),
            taskID=taskId)
        result["selectedCount"] = selected.count()
        if request.query_params.get("sqlJustShowSelected") == "true":
            selectedResult = {}
            result["results"] = [x['storeData'] for x in selected]

        # generating publics keys
        next = {}
        prev = {}
        next = request.query_params.dict()
        prev = request.query_params.dict()

        next["offsetcount"] = int(next["offsetcount"]) + int(next["nextcount"])
        next = urlencode(next)

        prev["offsetcount"] = int(prev["offsetcount"]) - int(prev["nextcount"])
        if prev["offsetcount"] < 0:
            prev["offsetcount"] = 0
        prev = urlencode(prev)

        result["next"] = request._request.META["HTTP_REFERER"] + request._request.META["PATH_INFO"][1::] + "?" + next
        result["prev"] = request._request.META["HTTP_REFERER"] + request._request.META["PATH_INFO"][1::] + "?" + prev

        # checking if data selected before or not
        # checking key field and check if selected or not

        result["extraCols"] = currentTaskDict.get("extraField")

        for r in result.get("results"):
            filter = {
                "sqlDataTableLinkerField": request.query_params.get("keyField"),
                "process": str(ProcessInstance.id),
                "sqlDataTableLinkerValue": r[request.query_params.get("keyField")], }
            sqlSelectedData = SqlTableSelectedItems.objects.filter(**filter)
            r["selectedBefore"] = bool(sqlSelectedData.count())
            r["extraValues"] = currentTaskDict.get("extraField")

            if r["selectedBefore"]:
                r["SqlTableSelectedItemID"] = str(sqlSelectedData.first().id)
                extraValues = None
                extraValues = ExtraSqlDataForTableSelectedItems.objects.filter(
                    sqlTableSelectedItemsLink=r["SqlTableSelectedItemID"])
                if extraValues.count() > 0:
                    r["extraValues"] = extraValues.first().values

        return Response(result)

    @list_route(methods=['get'])
    def Inbox(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        item_per_page = request.GET.get('itemPerPage')

        if item_per_page and not item_per_page == 'undefined':
            self.pagination_class.page_size = item_per_page

        if query and not query == 'undefined':
            search_text = request.GET['query']
            queryset = LunchedProcess.objects.filter(
                (Q(name__icontains=search_text) | Q(positionName__icontains=search_text)) & Q(isHide=False))
        else:
            queryset = LunchedProcess.objects.filter(isHide=False)
        posistionId = PositionsDocument.objects.get(userID=request.user.id, companyID=request.user.current_company.id)
        # try:
        # counterObj = Statistic.objects.get(position_id=posistionId.id)
        # except:
        # counterObj = Statistic(position_id=posistionId.id)
        #
        # counterObj.newLp = 0
        # counterObj.save()
        queryset = queryset.filter(thisPerformers__contains=str(posistionId.id))
        queryset = queryset.order_by('-postDate')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = LPInboxSerializer(page, many=True, request=request, currentPositionObj=posistionId)
            return self.get_paginated_response(serializer.data)

        serializer = LPInboxSerializer(queryset, many=True, request=request, currentPositionObj=posistionId)
        return Response(serializer.data)

    def getFilledForm(self, instance, newData):
        oldData = instance.formData
        for itm in newData.keys():
            oldData[itm] = newData[itm]
        return oldData

    def runCode(self, taskID, LauncedProcessInstance, beforeTask=True):
        for task in LauncedProcessInstance.bpmn.get("form"):
            if task['bpmnObjID'] == taskID:
                if beforeTask:
                    if task.get("oncreate"):
                        try:
                            UserTaskScriptLauncher(self, taskID, LauncedProcessInstance, task).do(task.get("oncreate"))
                        except Exception as e:
                            raise Exception(
                                "onCreate error : " + e + "\n\n\n\n\n\n" + task.get("oncreate") + "\n\n\n\n\n\n")
                if not beforeTask:
                    if task.get("onsend"):
                        try:
                            UserTaskScriptLauncher(self, taskID, LauncedProcessInstance, task).do(task.get("onsend"))
                        except Exception as e:
                            raise Exception(
                                "onCreate error : " + +e + "\n\n\n\n\n\n" + task.get("onsend") + "\n\n\n\n\n\n")

    @detail_route(methods=['patch'])
    def CompleteJob(self, request, *args, **kwargs):
        if not hasattr(self, "request"):
            self.request = request
            self.request.parser_context = {}
            self.request.parser_context["args"] = {}
            self.request.parser_context["kwargs"] = kwargs
            self.request.parser_context["request"] = request
            self.request.parser_context["view"] = self

        instance = self.get_object()
        newData = {}
        newData['formData'] = self.getFilledForm(instance, request.data['formData'])
        newData['bpmn'] = instance['bpmn']
        curId = str(PositionsDocument.objects.get(userID=request.user.id, companyID=request.user.current_company.id).id)
        newData = self.fill_new_schema(instance, curId, request.data['formSchema']['fields'], newData)
        taskID = request.data['taskID']

        # running before send python codes :
        self.runCode(taskID, instance, beforeTask=True)

        # request.data['seen']=False

        serializer = LunchedProcessSerializer(instance, data=newData, partial=True)

        serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer) commented bt mrb because of err 14524
        self.perform_update(serializer)  # BY MRB 1-9-1394
        enginefileClass = BpmsFileViewSet()
        engineInstance = pickle.loads(enginefileClass.getEngineTempFile(instance.engineInstance))
        engineInstance.keep_going(request, instance.formData)

        posistionId = PositionsDocument.objects.get(userID=request.user.id, companyID=request.user.current_company.id)
        # try:
        # counterObj = Statistic.objects.get(position_id=posistionId.id)
        # except:
        # counterObj = Statistic(position_id=posistionId.id)
        #
        # counterObj.Lp -= 0
        # counterObj.save()

        self.runCode(taskID, instance, beforeTask=False)

        return Response(serializer.data)

    @detail_route(methods=['patch'])
    def JustSaveIt(self, request, *args, **kwargs):
        instance = self.get_object()
        newData = {}
        newData['formData'] = self.getFilledForm(instance, request.data['formData'])
        newData['bpmn'] = instance['bpmn']
        curId = str(PositionsDocument.objects.get(userID=request.user.id, companyID=request.user.current_company.id).id)

        newData = self.fill_new_schema(instance, curId, request.data['formSchema']['fields'], newData)

        serializer = self.get_serializer(instance, data=newData, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def fill_new_schema(self, instance, curId, newSchema, newData):
        thisTask = ''
        if instance.thisSteps == None:
            instance.thisSteps = []
            instance.save()

        for itm in instance.thisSteps:
            if curId in itm.keys():
                thisTask = itm[curId]
                break
        i = 0
        for itm in newData['bpmn']['form']:
            if itm['bpmnObjID'] == thisTask:
                newData['bpmn']['form'][i]['schema']['fields'] = newSchema
                break
            i += 1
        return newData

    @detail_route(methods=['delete'])
    def HideLunchedProcess(self, request, *args, **kwargs):
        instance = self.get_object()
        itemForDelete = LunchedProcessArchive.objects.filter(lunchedProcessId=instance.id)
        itemForDelete2 = BigArchive.objects.filter(processId=instance.id)
        if itemForDelete.count() > 0:
            for _obj in itemForDelete:
                _obj.isHide = True
                _obj.save()
                _obj.formData['isDeleted'] = 1
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
                    # counterObj = Statistic.objects.get(position_id=_obj.performer)
                    # except:
                    # counterObj = Statistic(position_id=_obj.performer)
                    # counterObj.Mp += 1
                    # counterObj.newMp += 1
                    # counterObj.save()
        if itemForDelete2.count() > 0:
            for _obj in itemForDelete2:
                _obj.delete()
        serializer = self.get_serializer(instance, data={'isHide': True}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(1)

    def template_view_process_base(self, request, *args, **kwargs):
        return render_to_response('Bpms/BaseProcess.html', {},
                                  context_instance=RequestContext(request))

    def template_view_inbox(self, request, *args, **kwargs):
        return render_to_response('Bpms/BaseLunchedProcessInbox.html', {},
                                  context_instance=RequestContext(self.request))

    def template_view_do_process(self, request, *args, **kwargs):
        return render_to_response('Bpms/DoLunchedProcess.html', {},
                                  context_instance=RequestContext(request))

    def template_view_new_process(self, request, *args, **kwargs):
        return render_to_response('Bpms/NewLunchedProcess.html', {},
                                  context_instance=RequestContext(request))

    def template_view_diagram_process(self, request, *args, **kwargs):
        return render_to_response('Bpms/GetProcessDiagram.html', {},
                                  context_instance=RequestContext(request))

    def template_view_track_lunched_process(self, request, *args, **kwargs):
        return render_to_response('Bpms/TrackLunchedProcess.html', {},
                                  context_instance=RequestContext(request))

    def template_view_track_done_process(self, request, *args, **kwargs):
        return render_to_response('Bpms/TrackDoneProcess.html', {},
                                  context_instance=RequestContext(request))
