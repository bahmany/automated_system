# -*- coding: utf-8
import io
import os
import pickle
import sys
import xml.etree.ElementTree as ET
from copy import copy
from datetime import datetime, timedelta

from asq.initiators import query
from bson import ObjectId

from amspApp.BPMSystem.MyEngine.MyPackager import MyPackager
from amspApp.BPMSystem.MyEngine.ServiceTaskLuncher import ServiceTaskLauncher
from amspApp.BPMSystem.models import LunchedProcess, LunchedProcessArchive, Statistic, BigArchive, \
    ReportBpmnsPermissions, ReportData
from amspApp.BPMSystem.serializers.BigArchiveSerializer import BigArchiveSerializer
from amspApp.BPMSystem.serializers.DoneProcessArchiveSerializer import DoneProcessArchiveSerializer
from amspApp.BPMSystem.serializers.LunchedProcessArchiveSerializer import LunchedProcessArchiveSerializer
from amspApp.BPMSystem.serializers.LunchedProcessSerializer import LunchedProcessSerializer
from amspApp.BPMSystem.serializers.MessageProcessSerializer import MessageProcessSerializer
from amspApp.CompaniesManagment.Charts.models import Chart
from amspApp.CompaniesManagment.Charts.serializers.ChartSerializers import ChartSerializer
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.FileServer.views.BpmsFileView import BpmsFileViewSet
from amspApp.Infrustructures.MySpiffWorkflow import Task
from amspApp.Infrustructures.MySpiffWorkflow.bpmn.BpmnWorkflow import BpmnWorkflow
from amspApp.Infrustructures.MySpiffWorkflow.bpmn.specs.CallActivity import CallActivity as CallActivityBpmn
from amspApp.Infrustructures.MySpiffWorkflow.bpmn.specs.NoneTask import NoneTask as NoneTaskSpecBpmn
from amspApp.Infrustructures.MySpiffWorkflow.bpmn.specs.ServiceTask import ServiceTask
from amspApp.Infrustructures.MySpiffWorkflow.bpmn.specs.UserTask import UserTask as UserTaskSpecBpmn
from amspApp.Infrustructures.MySpiffWorkflow.bpmn.storage.BpmnSerializer import BpmnSerializer
from amspApp.Infrustructures.MySpiffWorkflow.specs.StartTask import StartTask as StartTaskREAL
from amspApp.Notifications.models import Notifications
from amspApp.Notifications.serializers.NotificationSerializer import NotificationsSerializer
from amspApp.Notifications.views.NotificationView import NotificationViewSet

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../lib'))


class BpmEngine(object):
    def changeProcessName(self, xml, newName):
        bpmn = ET.fromstring(xml)
        process = bpmn[len(bpmn) - 2]
        process.set('id', newName)
        return bpmn

    def __init__(self, lp_instance):
        """
        :param lp_instance: LunchedProcess object
        self.subProcess: this variable structure is like blew:
                        {"STEP NAME":{"form":"FORM SCHEMA","userTasks":"USER TASK DATA","id":"BPMN ID","xml":"XML"}}
        """
        self.serializer = BpmnSerializer()
        self.package = io.BytesIO()
        bpmn = self.changeProcessName(lp_instance.bpmn["xml"], str(lp_instance.id))
        # self.lp_instance = lp_instance
        self.forms = lp_instance.bpmn["form"]
        self.taskObjId = lp_instance.pk
        self.userTasks = lp_instance.bpmn["userTasks"]
        self.otherTasks = lp_instance.bpmn.get("otherTasks")
        package = MyPackager(self.package, str(lp_instance.pk))
        self.xml = lp_instance.bpmn["xml"]
        package.add_bpmn_file(bpmn)
        self.binding = lp_instance.bpmn['bindingMap']
        package.create_package_xml()
        self.wf_spec = self.serializer.deserialize_workflow_spec(self.package)
        # self.taken_path = self.track_workflow(self.wf_spec)
        self.workflow = BpmnWorkflow(self.wf_spec)
        self.subProcess = {}
        self.prev_detail = {}

    def get_this_performers(self, obj, userTask):
        """
            Usage of this function:
                you will need this when you want to get a list of performers
                for current steps

            :param obj: LunchedProcess document
            :param userTask:
            :param thisPerformers: performers list for this step
            :return: --> list of performers

            Mapping for if:
                1 --> assign whit select user
                2 --> assign whit select chart
                3 --> assign starter of process
                4 --> assign whit select group
                5 --> assign starters boss as performer
                6 --> assign performer according to form data
                7 --> assign performer according to chart rank
        """
        userTask['performerType'] = int(userTask['performerType'])
        thisPerformers = []
        if userTask['performerType'] == 1:
            thisPerformers = self._assign_selected_user(thisPerformers, userTask)

        elif userTask['performerType'] == 2:
            thisPerformers = self._assign_selected_chart(thisPerformers, userTask)

        elif userTask['performerType'] == 3:
            thisPerformers = self._assign_process_starter(thisPerformers, obj)

        elif userTask['performerType'] == 4:
            # still nothing considered
            pass

        elif userTask['performerType'] == 5:
            thisPerformers = self._assign_starter_boss(thisPerformers, obj)

        elif userTask['performerType'] == 6:
            thisPerformers = self._assign_form_selected_user(thisPerformers, obj, userTask)

        elif userTask['performerType'] == 7:
            thisPerformers = self._assign_starter_boss_rank(thisPerformers, obj, userTask)

        return thisPerformers

    def get_prev_performers_detail(self, obj, userTask, request):
        """
            Usage of this function:
                you will need this when you want to get a list of performers
                for current steps

            :param obj: LunchedProcess document
            :param userTask:
            :param thisPerformers: performers list for this step
            :return: --> list of performers

            Mapping for if:
                1 --> assign whit select user
                2 --> assign whit select chart and system find most free person in this chart as performer
                3 --> assign starter of process
                4 --> assign whit select group and system find most free person in this group as performer
                5 --> assign starters boss as performer
                6 --> assign performer according to form data
                7 --> assign performer according to chart rank
        """
        currPos = PositionsDocument.objects.get(companyID=request.user.current_company.id,
                                                userID=request.user.id)
        userTask['performerType'] = int(userTask['performerType'])
        thisPerformersNames = []
        if userTask['performerType'] == 1:
            thisPerformersNames = self._assign_selected_user_name(thisPerformersNames, userTask, str(currPos.id))
        elif userTask['performerType'] == 2:
            thisPerformersNames = self._assign_selected_chart_name(thisPerformersNames, userTask, str(currPos.id))
        elif userTask['performerType'] == 3:
            thisPerformersNames = self._assign_process_starter_name(thisPerformersNames, obj, str(currPos.id))
        elif userTask['performerType'] == 4:
            # still nothing considered
            pass
        elif userTask['performerType'] == 5:
            thisPerformersNames = self._assign_starter_boss_name(thisPerformersNames, obj, str(currPos.id))
        elif userTask['performerType'] == 6:
            thisPerformersNames = self._assign_form_selected_user_name(thisPerformersNames, obj, userTask,
                                                                       str(currPos.id))

        elif userTask['performerType'] == 7:
            thisPerformersNames = self._assign_starter_boss_name_by_rank(thisPerformersNames, obj, str(currPos.id),
                                                                         userTask)
        return thisPerformersNames

    def get_this_steps(self, performers, userTask, thisSteps=None):
        if thisSteps == None:
            thisSteps = []
        for itm in performers:
            thisSteps.append({itm: userTask['taskId']})
        return thisSteps

    def get_last_change_date(self, performers, thisDates=None):
        if thisDates == None:
            thisDates = []
        for itm in performers:
            thisDates.append({itm: datetime.now()})
        return thisDates

    def prepare_seen_date_field(self, performers, seenDate=None):
        if seenDate == None:
            seenDate = []
        for itm in performers:
            seenDate.append({itm: 0})
        return seenDate

    def get_performer_type(self, performers, userTask, performerType=None):
        if performerType == None:
            performerType = []
        for itm in performers:
            performerType.append({itm: userTask['performerType']})
        return performerType

    def get_this_charts(self, performers, chartPerformer=None):
        if chartPerformer == None:
            chartPerformer = []
        for itm in performers:
            currentPos = PositionsDocument.objects.get(id=itm)  # exception here means no performer selected ...
            chartPerformer.append({itm: currentPos.chartID, 'title': currentPos.chartName})
        return chartPerformer

    def get_this_charts_list(self, performers, chartPerformer=None):
        if chartPerformer == None:
            chartPerformer = []
        for itm in performers:
            currentPos = PositionsDocument.objects.get(id=itm)
            chartPerformer.append(currentPos.chartID)
        return chartPerformer

    def get_this_steps_names(self, performers, userTask, userTaskSpec, thisStepsNames=None):
        if thisStepsNames == None:
            thisStepsNames = []
        # chartTitle is the current chart title
        if not 'selectedBAM' in userTask or userTask['selectedBAM'] == '':
            selectedBAM = -1
            selectedBAMDate = datetime.now() + timedelta(days=365)
        else:
            selectedBAM = userTask['selectedBAM']
            selectedBAMDate = datetime.now() + timedelta(hours=userTask['selectedBAM'])
        for itm in performers:
            currentPos = PositionsDocument.objects.get(id=itm)
            thisStepsNames.append({itm: userTaskSpec.description, 'prev': userTaskSpec.inputs[0].description,
                                   'chartId': currentPos.chartID, 'chartTitle': currentPos.chartName,
                                   'id': userTaskSpec.name, 'positionName': currentPos.profileName,
                                   'selectedBAM': selectedBAM, 'selectedBAMDate': selectedBAMDate,
                                   'avatar': currentPos.avatar})
        return thisStepsNames

    def update_statistics_lp_increase(self, performers):
        """
        Usage:
            when some performers have new task in their inbox
            this func will increase inbox task counter for performer
        :param performers:
        :return:
        """
        for itm in performers:
            try:
                counterObj = Statistic.objects.get(position_id=ObjectId(itm))
            except:
                counterObj = Statistic(position_id=ObjectId(itm))
            counterObj.Lp += 1
            counterObj.newLp += 1
            counterObj.save()

    def update_statistics_mp_increase(self, receiver):
        """
        Usage:
            when some performers have new message in their inbox
            this func will increase message inbox counter for receivers
        :param receiver:
        :return:
        """
        try:
            counterObj = Statistic.objects.get(position_id=ObjectId(receiver))
        except:
            counterObj = Statistic(position_id=ObjectId(receiver))
        counterObj.Mp += 1
        counterObj.newMp += 1
        counterObj.save()

    def update_statistics_Lp_done_reduce(self, performers):
        """
        Usage:
            when some performers have done his task
            this func will reduce task inbox counter for performer
        :param performers:
        :return:
        """
        for itm in performers:
            try:
                counterObj = Statistic.objects.get(position_id=ObjectId(itm))
            except:
                counterObj = Statistic(position_id=ObjectId(itm))
            counterObj.Lp -= 1
            counterObj.save()

    def create_lpa(self, obj, currentPosition, stepName, msgStep=None):
        """
        Usage:
            when it was needed to create a lunchedProcessArchive object
        """
        if obj.thisSteps:
            stepsForCreateLpa = obj.thisSteps
        else:
            stepsForCreateLpa = []
        if msgStep:
            stepsForCreateLpa.append({str(currentPosition): msgStep})
        stepsWithDates = {}
        steps = []
        for stp in stepsForCreateLpa:
            if str(currentPosition.id) in stp.keys():
                stpName = stp[str(currentPosition.id)]
                stepsWithDates[stpName] = {"comeToInbox": obj.lastInboxChangeDate,
                                           "done": datetime.now()}
                steps.append(stpName)
        prevPerformer = {}
        for itm in obj.PrevPerformersDetail:
            if str(currentPosition.id) in itm.keys():
                prevPerformer['name'] = itm[str(currentPosition.id)]
                prevPerformer['avatar'] = itm['avatar']
                prevPerformer['chartTitle'] = itm['chartTitle']
            break
        data = {
            'user_id': obj.user_id,
            'position_id': obj.position_id,
            'positionName': obj.positionName,
            'chartTitle': obj.chartTitle,
            'positionPic': obj.positionPic,
            'lastUrStepName': stepName,
            'lastUrPrevPerformerName': prevPerformer['name'] if 'name' in prevPerformer else '-----',
            'bpmnName': obj.bpmn['name'],
            'chartId': obj.chartId,
            'lunchedProcessId': obj.id,
            'bpmn': obj.bpmn,
            'name': obj.name,
            'stepsWithDates': stepsWithDates,
            'performer': currentPosition.id,
            'chartPerformer': currentPosition.chartID,
            'prevPerformer': prevPerformer,
            'pastSteps': obj.id,
            'steps': steps,
            'formData': obj.formData,
            'startProcessDate': obj.postDate,
            'postDate': datetime.now()
        }
        serializer = LunchedProcessArchiveSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def update_lpa(self, objForUpdate, obj, currentPosition, stepName, msgStep=None):
        """
        Usage:
            when it was needed to update a lunchedProcessArchive object
        """
        stepsForUpdateLpa = obj.thisSteps
        if stepsForUpdateLpa == None:
            stepsForUpdateLpa = []
        if msgStep:
            stepsForUpdateLpa.append({str(currentPosition.id): msgStep})
        stepsWithDates = objForUpdate.stepsWithDates
        steps = objForUpdate.steps
        for stp in stepsForUpdateLpa:
            if str(currentPosition.id) in stp.keys():
                stpName = stp[str(currentPosition.id)]
                stepsWithDates[stpName] = {"comeToInbox": obj.lastInboxChangeDate, "done": datetime.now()}
                steps.append(stpName)
        prevPerformer = {}
        for itm in obj.PrevPerformersDetail:
            if str(currentPosition.id) in itm.keys():
                prevPerformer['name'] = itm[str(currentPosition.id)]
                prevPerformer['avatar'] = itm['avatar']
                prevPerformer['chartTitle'] = itm['chartTitle']
            break
        data = {
            'formData': obj.formData,
            'lastUrStepName': stepName,
            'stepsWithDates': stepsWithDates,
            'prevPerformer': prevPerformer,
            'lastUrPrevPerformerName': prevPerformer['name'] if 'name' in prevPerformer else '-----',
            'postDate': datetime.now(),
            'steps': steps
        }

        serializer = LunchedProcessArchiveSerializer(objForUpdate, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def get_correct_prev_detail(self, performersList, taskID):
        res = []
        prevD = self.prev_detail
        oldKeys = list(self.prev_detail.keys())
        for itm in performersList:
            if len(oldKeys) > 0:
                oldPosId = ''
                for itm2 in oldKeys:
                    if not itm2 == 'id' and not itm2 == 'avatar' and not itm2 == 'chartTitle':
                        oldPosId = itm2
                        break
                res.append({itm: self.prev_detail[oldPosId],
                            'avatar': self.prev_detail['avatar'],
                            'chartTitle': self.prev_detail['chartTitle'],
                            'id': self.prev_detail['id'],
                            'taskID': taskID})

        return res

    def update_lp(self, ut, obj, workflowUt=None):
        """
        @:param ut: object that i store in Bpmn document for user tasks that bpmn designer have designed form and things for it.
        @:param workflowUt: object that workflow engine has parsed it (t.task_spec)[now i use it for persian(not id) name of steps]
        @:param obj: lunched process object
        Usage:
            when it was needed to update a lunchedProcess object
        """
        oldPerformersList = obj.thisPerformers
        oldPrevDet = obj.PrevPerformersDetail

        performersList = self.get_this_performers(obj, ut)
        performersList = query(performersList).distinct().to_list()

        # there are just new performers for this step (ut)
        NewPerformersList = copy(performersList)
        prevDetList = self.get_correct_prev_detail(performersList, ut.get("taskId"))

        # stepHistory = obj.StepHistory
        # cc = copy(self.prev_detail)
        # cc.update({"taskID": ut.get("taskId"), "dateOfRun":datetime.now()})
        #
        # stepHistory.append(cc)

        for itm in oldPerformersList:
            performersList.append(itm)
        for itm in oldPrevDet:
            prevDetList.append(itm)
        data = {
            'thisPerformers': performersList,
            'PrevPerformersDetail': prevDetList,
            'thisPerformerType': self.get_performer_type(NewPerformersList, ut, copy(obj.thisPerformerType)),
            'thisChartPerformer': self.get_this_charts(NewPerformersList, copy(obj.thisChartPerformer)),
            'thisChartList': self.get_this_charts_list(NewPerformersList, copy(obj.thisChartList)),
            'thisSteps': self.get_this_steps(NewPerformersList, ut, copy(obj.thisSteps)),
            'thisStepsNames': self.get_this_steps_names(NewPerformersList, ut, workflowUt, copy(obj.thisStepsNames)),
            'lastInboxChangeDate': self.get_last_change_date(NewPerformersList, copy(obj.lastInboxChangeDate)),
            'seen': self.prepare_seen_date_field(NewPerformersList, copy(obj.seen))
        }

        serializer = LunchedProcessSerializer(obj, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def create_big_archive(self, obj, bpmnCompId):
        for itm in obj.thisStepsNames:
            performerId = ''
            for itm2 in itm.keys():
                if not itm2 == 'prev' and not itm2 == 'chartId' and not itm2 == 'chartTitle' and not itm2 == 'selectedBAM' and not itm2 == 'selectedBAMDate' and not itm2 == 'avatar' and not itm2 == 'id' and not itm2 == 'positionName':
                    performerId = itm2
                    break

            stepName = itm[performerId]
            positionName = itm['positionName']
            chartTitle = itm['chartTitle']
            avatar = itm['avatar']
            stepId = itm['id']
            prevStepName = itm['prev']
            prevPerformer = {
                'name': '',
                'avatar': '',
                'chartTitle': '',
                'id': '',
            }
            for itm3 in obj.PrevPerformersDetail:
                if performerId in itm3.keys():
                    prevPerformer['name'] = itm3[performerId]
                    prevPerformer['avatar'] = itm3['avatar']
                    prevPerformer['chartTitle'] = itm3['chartTitle']
                    prevPerformer['id'] = itm3['id']
                    break
            data = {
                'bpmnName': obj.bpmn['name'],
                'bpmnId': ObjectId(obj.bpmn['id']),
                'processId': obj.id,
                'companyId': bpmnCompId,
                'taskId': stepId,
                'taskName': stepName,
                'startDate': obj.postDate,
                'postDate': datetime.now(),
                'prevPerformer': prevPerformer,
                'starterId': obj.position_id,
                'starterName': obj.positionName,
                'prevStepName': prevStepName,
                'starterChartName': obj.chartTitle,
                'thisPerformerId': performerId,
                'thisPerformerName': positionName,
                'BAMHours': itm['selectedBAM'],
                'BAMDate': itm['selectedBAMDate'],
                'thisPerformerAvatar': avatar,
                'isStepDone': False,
                'isProcessDone': False,
                'thisPerformerChartName': chartTitle,
                'isChild': True if obj.childId else False,
                'parentProcessId': obj.parentId,
                'parentProcessName': obj.parentBpmnName,
                'childProcessId': obj.childId
            }

            serializer = BigArchiveSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.create(serializer.validated_data)

    def setReportsThingsPerChartID(self, currentPosition, obj, request):
        """
        :param currentPosition:----
        :param obj:  LP Object
        :param request: ---
        :return:
        USAGE:
            it runs for create permissions and data for bpms report system...
            and it creates permissions and data per chartId

        """
        chartIds = ChartSerializer().get_list_top_chart_from_chartID(currentPosition.chartID)
        for itmID in chartIds:
            # create bpmn list for getting reports permissions that implement how can get report from which bpmn
            self.setReportsBpmnPermission(itmID, currentPosition, obj)

            # create data reports it implement how can get report from which data
            self.createReportsData(itmID, currentPosition, obj, request)

    def createReportsData(self, itmID, currentPosition, obj, request):
        """
        :param itmID: chartID
        :param currentPosition:
        :param obj: LP object
        :param request:--
        :return:
        USAGE:
            create object contains form data for getting better and faster reports
        """
        try:
            objForUpf = ReportData.objects.get(chartId=int(itmID),
                                               lpId=obj.id)
            formData = objForUpf.formData
            newFormData = request.data['formData']
            for itm in newFormData.keys():
                formData[itm] = newFormData[itm]
            objForUpf.formData = formData
            objForUpf.save()

        except:
            newPermissionsf = ReportData(chartId=int(itmID),
                                         lpId=obj.id,
                                         lpName=obj.name,
                                         companyId=currentPosition.companyID,
                                         bpmnId=ObjectId(obj.bpmn['id']),
                                         bpmnName=obj.bpmn['name'],
                                         lpStartDate=obj.postDate,
                                         lpEndDate=obj.postDate,
                                         lpPosition=obj.position_id,
                                         lpPositionName=obj.positionName,
                                         lpChart=obj.chartId,
                                         lpChartName=obj.chartTitle,
                                         processObjs=obj.bpmn['processObjs'],
                                         formData={})
            formData = newPermissionsf.formData
            newFormData = request.data['formData']
            for itm in newFormData.keys():
                formData[itm] = newFormData[itm]
            newPermissionsf.formData = formData
            newPermissionsf.save()

    def setReportsBpmnPermission(self, itmID, currentPosition, obj):
        """
        :param itmID: chartID
        :param currentPosition:
        :param obj: LP object
        :return:
        USAGE:
            create object contains bpmns which u can have access to them for getting better and faster results
        """

        try:
            objForUp = ReportBpmnsPermissions.objects.get(chartId=int(itmID),
                                                          companyId=currentPosition.companyID)
            if not obj.bpmn['id'] in objForUp.bpmns:
                objForUp.bpmns.append(obj.bpmn['id'])
                objForUp.bpmnsDetail.append({"id": obj.bpmn['id'], "name": obj.bpmn['name']})
                objForUp.save()

        except:
            newPermissions = ReportBpmnsPermissions(chartId=int(itmID),
                                                    companyId=currentPosition.companyID,
                                                    bpmns=[obj.bpmn['id']],
                                                    bpmnsDetail=[
                                                        {'id': obj.bpmn['id'], 'name': obj.bpmn['name']}])
            newPermissions.save()
            # width: 120px;
            # white-space: nowrap;
            # overflow: hidden !important;
            # text-overflow: ellipsis;

    def createNotification(self, notifType, usersPosId, bpmnName, stepName, objId):
        """
        :param notifType:--
        :param usersPosId: list of users who should get this notification
        :param bpmnId: --
        :param bpmnName: --
        :param stepName: -- stepName=None when it's a done job
        :param objId: LP id when it's running ... and DPA id when it's done
        :return:
        """
        baseData = {}
        data = {}
        data['objId'] = objId
        data['bpmnName'] = bpmnName
        data['stepName'] = stepName
        baseData["type"] = notifType
        baseData["typeOfAlarm"] = 1
        baseData["periority"] = 1
        baseData["informType"] = 1
        for posId in usersPosId:
            posDocument = PositionsDocument.objects.get(id=ObjectId(posId))
            baseData["userID"] = posDocument.userID
            if notifType == 2:
                self.createNotificationNewJob(posDocument, baseData, data)
            elif notifType == 3:
                self.createNotificationNewMessage(posDocument, baseData, data)
                # else:
                # self.createNotificationDoneJob(posDocument, baseData, data)

    def createNotificationNewJob(self, currentPos, baseData, data):
        extra = {}
        titlePrefix = 'کار '
        titleMidix = ' از '
        extra["url"] = '/dashboard/Process/Inbox/' + data['objId'] + '/Do'
        extra["title"] = titlePrefix + data['stepName'] + titleMidix + data['bpmnName']
        extra["currentCompany"] = currentPos.companyID
        extra["chartName"] = currentPos.chartName
        extra["profileName"] = currentPos.profileName
        extra["currentCompanyName"] = currentPos.companyName
        extra["ownerPositionID"] = str(currentPos.id)
        baseData['extra'] = extra
        vs = NotificationsSerializer(data=baseData)
        vs.is_valid(raise_exception=True)
        vs.save()
        return vs

    #
    # def createNotificationDoneJob(self, currentPos, baseData, data):
    # extra = {}
    # titlePrefix = 'فرایند '
    # titleMidix = 'پایان یافت'
    # extra["url"] = '/dashboard/Process/DoneArchive/' + data['objId'] + '/TrackDoneProcess'
    # extra["title"] = titlePrefix + data['bpmnName'] + titleMidix
    # extra["currentCompany"] = currentPos.companyID
    # extra["chartName"] = currentPos.chartName
    # extra["profileName"] = currentPos.profileName
    # extra["currentCompanyName"] = currentPos.companyName
    # extra["ownerPositionID"] = str(currentPos.id)
    # baseData['extra'] = extra
    # vs = NotificationsSerializer(data=baseData)
    # vs.is_valid(raise_exception=True)
    # vs.save()
    # return vs

    def createNotificationNewMessage(self, currentPos, baseData, data):
        extra = {}
        titlePrefix = 'پیام '
        titleMidix = ' از '
        extra["url"] = '/dashboard/Process/Message/' + data['objId'] + '/DoMessage'
        extra["title"] = titlePrefix + data['stepName'] + titleMidix + data['bpmnName']
        extra["currentCompany"] = currentPos.companyID
        extra["chartName"] = currentPos.chartName
        extra["profileName"] = currentPos.profileName
        extra["currentCompanyName"] = currentPos.companyName
        extra["ownerPositionID"] = str(currentPos.id)
        baseData['extra'] = extra
        vs = NotificationsSerializer(data=baseData)
        vs.is_valid(raise_exception=True)
        vs.save()
        return vs

    def update_big_archive(self, obj, taskId, taskName, currentPosition, request):
        """

        :param obj: LP Obj
        :param taskId: id of task that just have done
        :param taskName: name of task that just have done
        :param currentPosition: ---
        :param request: ---
        :return: updated BigArchive object or 'ERROR'

        USAGE:
            it'll be run when someone do his/her job(task)...
            and it update bigArchive for this step to done
        """
        try:
            objForUpdate = BigArchive.objects.get(processId=obj.id, taskId=taskId, isStepDone=False)
            thisSchema = {}
            thisSchemaFileds = []
            formsList = obj.bpmn['form']
            for itm in formsList:
                if itm['bpmnObjID'] == taskId:
                    fieldsList = itm['schema']['fields']
                    for itm3 in fieldsList:
                        thisSchema['type'] = itm3['type']
                        thisSchema['name'] = itm3['name']
                        thisSchemaFileds.append(itm3['name'])
                        thisSchema['displayName'] = itm3['displayName']
                    break
            data = {
                'isStepDone': True,
                'thisForm': thisSchemaFileds,
                'thisPerformerChartId': currentPosition.chartID,
                'doneDate': datetime.now(),
            }

            serializer = BigArchiveSerializer(objForUpdate, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            updatedArc = BigArchiveSerializer().update(instance=objForUpdate, validated_data=serializer.validated_data)

            # create data and permission for reports per chartID
            self.setReportsThingsPerChartID(currentPosition, obj, request)

            return updatedArc
        except:
            return 'error'

    def set_big_archive_done_process(self, obj):
        """

        :param obj:LP object which going to finish(done) in a minute
        :return:
        USAGE:
            make all bigArchive objects to done process
        """

        objForUpdate = BigArchive.objects.filter(processId=obj.id, isProcessDone=False)
        data = {
            'isProcessDone': True
        }
        for itm in objForUpdate:
            serializer = BigArchiveSerializer(itm, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return 1

    def create_mp(self, obj, receiver, currentPosition, currentStep, tSpec):
        """
        Usage:
            when it was needed to create a messageProcess object
            in order to make an message object in message's inbox
            of receiver
        """
        thisPos = PositionsDocument.objects.get(id=ObjectId(receiver))
        prevPerformer = {}
        prevPerformer['name'] = currentPosition.profileName
        prevPerformer['avatar'] = currentPosition.avatar
        prevPerformer['chartTitle'] = currentPosition.chartName
        data = {
            'user_id': obj.user_id,
            'positionName': obj.positionName,
            'positionPic': obj.positionPic,
            'chartTitle': obj.chartTitle,
            'chartId': obj.chartId,
            'position_id': obj.position_id,
            'lunchedProcessId': obj.id,
            'bpmn': obj.bpmn,
            'bpmnForCreate': obj.bpmnForCreate,
            'name': obj.name,
            'thisStep': currentStep['taskId'],
            'thisStepName': tSpec.description,
            'prevStep': tSpec.inputs[-1].name,
            'prevStepName': tSpec.inputs[-1].description,
            'thisPerformer': receiver,
            'performerDetail': prevPerformer,
            'pastSteps': obj.pastSteps,
            'startProcessDate': obj.postDate,
            'formData': obj.formData,
        }
        serializer = MessageProcessSerializer(data=data)
        if serializer.is_valid():
            new = serializer.create(serializer.validated_data)
            self.createNotification(3, [str(thisPos.id)], obj.bpmn['name'], tSpec.description, str(new.id))

    def run_call_activity(self, t, obj, request):
        """
            Usage of this function:
                it's gonna run when workflow reaches to a call activity
                and it needs to setup some settings
                IN THE OTHER WORD:
                this function is gonna run when workflow is in a step that is
                a call activity
            ca==CallActivity
        """
        sub = {}
        caBinding = self.binding[t.task_spec.name]['fields']
        for itm in caBinding:
            # if it's a initializing data for called Process
            if (itm['fromBpmn'] == obj.bpmn['id']):
                sub[itm['toId']] = self.processData[itm['fromId']]

        data = {
            'bpmnForCreate': self.binding[t.task_spec.name]['bpmnSelected'],
            'name': '--',
            'parentId': obj.id,
            'parentBpmnName': obj.name,
            'formData': sub,
            'parentTaskId': t.task_spec.name
        }
        serializer = LunchedProcessSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new = serializer.createFromCallActivity(serializer.validated_data, request=request, parentObj=obj)
            engineInstance = BpmEngine(new)
            enginefileClass = BpmsFileViewSet()
            enginefileClass = enginefileClass.createEngineTempFile(pickle.dumps(engineInstance))
            new.engineInstance = enginefileClass
            new.save()
            engineInstance.run(request)
            childlist = obj.childId
            childlist = childlist.append(new.id)
            obj.childId = childlist
            obj.thisPerformers = []
            obj.save()
            enginefileClass = BpmsFileViewSet()
            enginefileClass = enginefileClass.updateEngineTempFile(obj.engineInstance,
                                                                   pickle.dumps(self))

    def do_call_activity(self, childObj, request):
        """
        :param obj: the child process
        :param request:
        :return:
        USAGE:
            it'll run when a call activity has done and need to continue from its parent
        """
        parentObj = LunchedProcess.objects.get(pk=childObj.parentId)
        enginefileClass = BpmsFileViewSet()
        engineInstance = pickle.loads(enginefileClass.getEngineTempFile(parentObj.engineInstance))
        engineInstance.keep_going_all_activity(childObj.parentTaskId)
        parentObj.pastSteps.append(childObj.parentTaskId)
        parentObj.save()
        toParent = {}
        caBinding = parentObj.bpmn['bindingMap'][childObj.parentTaskId]['fields']
        for itm in caBinding:
            # if it's a initializing data for called Process
            if itm['toBpmn'] == parentObj.bpmn['id']:
                toParent[itm['toId']] = self.processData[itm['fromId']]
        self.add_data_to_parent(parentObj, toParent)
        engineInstance.keep_going(request, callActivityFlag=True)

    def add_data_to_parent(self, parentObj, data):
        parentData = parentObj.formData
        for itm in data.keys():
            if itm in parentData.keys():
                parentObj.formData[itm] = data[itm]
        parentObj.save()

    def run_user_task(self, t, obj):
        """
            Usage of this function:
                it's gonna run when workflow needs to create a task in
                inbox tasks of this performer
                IN THE OTHER WORD:
                this function is gonna run when workflow is in a step that is
                a user task and it doesn't need any approve or these kind of things

        """
        bpmnCompId = Bpmn.objects.filter(id=ObjectId(obj.bpmnForCreate))[0].company_id
        for ut in self.userTasks:
            if ut['taskId'] == t.task_spec.name:
                self.update_lp(ut, obj, t.task_spec)
                enginefileClass = BpmsFileViewSet()
                enginefileClass = enginefileClass.updateEngineTempFile(obj.engineInstance,
                                                                       pickle.dumps(self))
                # self.update_statistics_lp_increase(obj.thisPerformers)
                self.createNotification(2, obj.thisPerformers, obj.bpmn['name'],
                                        t.task_spec.description, str(obj.id))
                self.create_big_archive(obj, bpmnCompId)
                # obj.save()

    def removeOldPorformers(self, oldPerformers, listForDel):
        """

        :param oldPerformers: list of pos id which should remove from listForDel(obj.* attrs)
        :param listForDel: it's a list that can be obj.thisSteps or obj.seen or obj.lastChangeInbox....
                and this func will remove the oldPerformers from this
        :return:correct list of attrs
        USAGE:
            i use this to remove old performers from LP obj attrs when someone do his/her task(step)
        """
        for itm in oldPerformers:
            i = 0
            for itm2 in listForDel:
                if itm in itm2.keys():
                    del listForDel[i]
                i = i + 1
        return listForDel

    def do_user_task(self, obj, request, t, currentPosition):
        """
        Usage of this function:
            it's gonna run when workflow needs to complete(do) a task by performer's click
            IN THE OTHER WORD:
            this function is gonna run when workflow is in a step that is
            a user task and it needs completion and do or these kind of things
        """
        posIdForDel = []
        strCurrentPositionId = str(currentPosition.id)
        posIdForDel.append(strCurrentPositionId)

        for mti in obj.thisPerformerType:
            if strCurrentPositionId in mti.keys():
                if mti[strCurrentPositionId] == 2:
                    posForDel = PositionsDocument.objects.filter(chartID=currentPosition.chartID)
                    for itm in posForDel:
                        if itm.id != currentPosition.id:
                            # =============================================Notification========
                            Notifications.objects.filter(type=2, extra__url='/dashboard/Process/Inbox/' + str(
                                obj.id) + '/Do').delete()
                            NotificationViewSet().changesHappened(itm.userID)
                            # =============================================Notification========
                            posIdForDel.append(str(itm.id))
                    break

        for ut in self.userTasks:
            if ut['taskId'] == t.task_spec.name:
                self.prev_detail = self.get_prev_performers_detail(obj, ut, request)
                # break MAYBE

        if strCurrentPositionId in obj.thisPerformers:
            # self.update_statistics_Lp_done_reduce(obj.thisPerformers)
            try:
                objForUpdate = LunchedProcessArchive.objects.get(lunchedProcessId=obj.id, performer=currentPosition.id)
                self.update_lpa(objForUpdate, obj, currentPosition, t.task_spec.description)
            except:
                self.create_lpa(obj, currentPosition, t.task_spec.description)

            # remove from obj.thisPerformers
            for itm in posIdForDel:
                obj.thisPerformers.remove(itm)

            obj.thisChartList.remove(int(currentPosition.chartID))

            obj.thisSteps = self.removeOldPorformers(posIdForDel, copy(obj.thisSteps))
            obj.PrevPerformersDetail = self.removeOldPorformers(posIdForDel, copy(obj.PrevPerformersDetail))
            obj.thisChartPerformer = self.removeOldPorformers(posIdForDel, copy(obj.thisChartPerformer))
            obj.thisPerformerType = self.removeOldPorformers(posIdForDel, copy(obj.thisPerformerType))
            obj.thisStepsNames = self.removeOldPorformers(posIdForDel, copy(obj.thisStepsNames))
            obj.lastInboxChangeDate = self.removeOldPorformers(posIdForDel, copy(obj.lastInboxChangeDate))
            obj.seen = self.removeOldPorformers(posIdForDel, copy(obj.seen))
            obj.allPerformers.append(strCurrentPositionId)
            obj.save()
            self.update_big_archive(obj, t.task_spec.name, t.task_spec.description, currentPosition, request)

        else:
            return 'you are not be able to access to this step'

    def run_message(self, t, obj, request):
        """
            Usage of this function:
                it's gonna run when workflow needs to send a message to the receivers
                IN THE OTHER WORD:
                this function is gonna run when workflow is in a step that is


         a none type task and it needs to just create a message object in
                the message's inbox of the person

        """
        for ut in self.userTasks:
            if ut['taskId'] == t.task_spec.name:
                currentPosition = PositionsDocument.objects.get(companyID=request.user.current_company.id,
                                                                userID=request.user.id)
                reciversOfMessage = self.get_this_performers(obj, ut)

                for rc in reciversOfMessage:
                    rcPos = PositionsDocument.objects.get(id=rc)
                    self.create_mp(obj, rc, currentPosition, ut, t.task_spec)  # updated by MRB 02/09/1394
                    # self.update_statistics_mp_increase(rc)
                    try:
                        objForUpdate = LunchedProcessArchive.objects.get(lunchedProcessId=obj.id,
                                                                         performer=ObjectId(rc))
                        self.update_lpa(objForUpdate, obj, rcPos, t.task_spec.description, ut['taskId'])
                    except:
                        self.create_lpa(obj, rcPos, t.task_spec.description, ut['taskId'])

    def run_on_workflow_completed(self, obj, request):
        """
            Usage of this function:
                it's gonna run when workflow was just completed(finished)

        """
        self.set_big_archive_done_process(obj)
        archiveObjs = LunchedProcessArchive.objects.filter(lunchedProcessId=obj.id)
        for itm in archiveObjs:
            lpObject = LunchedProcess.objects.get(id=itm.lunchedProcessId)
            data = {
                'user_id': itm.user_id,
                'position_id': itm.position_id,
                'positionName': itm.positionName,
                'positionPic': itm.positionPic,
                'bpmn': itm.bpmn,
                'chartTitle': itm.chartTitle,
                'bpmnName': itm.bpmnName,
                'lastUrStepName': itm.lastUrStepName,
                'name': itm.name,
                'lastUrPrevPerformerName': itm.lastUrPrevPerformerName,
                'stepsWithDates': itm.stepsWithDates,
                'performer': itm.performer,
                'chartPerformer': itm.chartPerformer,
                'pastSteps': lpObject.pastSteps,
                'steps': itm.steps,
                'prevPerformer': itm.prevPerformer if itm.prevPerformer else {},
                'formData': itm.formData,
                'startProcessDate': itm.startProcessDate,
                'lunchedProcessId': itm.lunchedProcessId,
                'postDate': datetime.now()
            }
            serializer = DoneProcessArchiveSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.create(serializer.validated_data)
            itm.delete()
        reportDataList = ReportData.objects.filter(lpId=obj.id)
        for itm2 in reportDataList:
            itm2.isDone = True
            itm2.save()
        if obj.parentId:
            self.do_call_activity(obj, request)

        obj.delete()

    def run(self, request):
        """
            Usage of this function:
                it's gonna run when a person start a process
                IN THE OTHER WORDS
                when someone wants to create new process
        """
        workflow = self.workflow
        condition_keys = []
        obj = LunchedProcess.objects.get(pk=self.taskObjId)
        currentPosition = PositionsDocument.objects.get(companyID=request.user.current_company.id,
                                                        userID=request.user.id)

        chartIds = ChartSerializer().get_list_top_chart_from_chartID(currentPosition.chartID)
        for itmID in chartIds:
            # create bpmn list for getting reports permissions that implement how can get report from which bpmn
            self.setReportsBpmnPermission(itmID, currentPosition, obj)

        obj.allPerformers.append(str(currentPosition.id))
        self.create_lpa(obj, currentPosition, 'شروع فرایند')
        while not workflow.is_completed():
            tasks = workflow.get_tasks(Task.READY)
            for t in tasks:
                self.processData = copy(obj.formData)
                t.set_data(**self.processData)
                if type(t.task_spec) == UserTaskSpecBpmn:
                    self.run_user_task(t, obj)
                    return
                if type(t.task_spec) == NoneTaskSpecBpmn:
                    self.run_message(t, obj, request)
                    break
                if type(t.task_spec) == CallActivityBpmn:
                    self.run_call_activity(t, obj, request)

                if hasattr(t.task_spec, "cond_task_specs"):
                    for cond, name in t.task_spec.cond_task_specs:
                        for cond_unit in cond.args:
                            if hasattr(cond_unit, "name"):
                                condition_keys.append(cond_unit.name)
                obj.pastSteps.append(t.task_spec.name)
                if type(t.task_spec) != StartTaskREAL:
                    for itm in t.task_spec.outgoing_sequence_flows_by_id.keys():
                        obj.pastSteps.append(itm)
                obj.save()
            workflow.complete_next()
        if workflow.is_completed():
            self.run_on_workflow_completed(obj, request)

    def keep_going(self, request=None, databaseData=None, callActivityFlag=False):
        """
            Usage of this function:
                it's gonna run when someone has done(completed)
                his task, and workflow needs to go ahead
        """
        workflow = self.workflow
        condition_keys = []
        # it for when a performer had two step in a row
        if callActivityFlag:
            flag = 1
        else:
            flag = 0
        obj = LunchedProcess.objects.get(pk=self.taskObjId)
        currentPosition = PositionsDocument.objects.get(companyID=request.user.current_company.id,
                                                        userID=request.user.id)
        strCurrentPositionId = str(currentPosition.id)
        SECURITYwhile = 0
        while not workflow.is_completed():
            SECURITYwhile += 1
            # it for when a do_user_task run and it should change the status of task
            flag2 = 0
            tasks = workflow.get_tasks(Task.READY)
            countTasks = len(tasks)
            countHasRun = 0
            countHasJumped = 0
            SECURITYfor = 0
            jumpFromThisTask = 0
            doneExactThisOne = 0
            doneExactThisOneTask = {}
            for t in tasks:
                SECURITYfor += 1
                self.processData = copy(obj.formData)
                if not self.processData == None:
                    t.set_data(**self.processData)
                # it will run when user would click on done
                if not flag:
                    for currentStep in obj.thisSteps:
                        if strCurrentPositionId in currentStep:
                            if currentStep[strCurrentPositionId] == t.task_spec.name:
                                if type(t.task_spec) == UserTaskSpecBpmn:
                                    self.do_user_task(obj, request, t, currentPosition)
                                    jumpFromThisTask = 0
                                    doneExactThisOne = t.id
                                    doneExactThisOneTask = t
                                    obj.pastSteps.append(t.task_spec.name)
                                    obj.save()

                                    flag = 1
                                    flag2 = 1
                                    break
                # it will break parent for only when the user click and the loop has run first time
                if flag2:
                    break
                else:

                    if type(t.task_spec) == ServiceTask:
                        serviceTask = ServiceTaskLauncher(currentPosition, currentStep, obj, t, request)
                        serviceTask.do()
                        pass

                    if type(t.task_spec) == UserTaskSpecBpmn:
                        # this for will check that this task has ever prepare for user tasks before or not!!
                        # (Has "self.run_user_task(t, obj)" run for this task or not ? )
                        flag3 = 0
                        jumpFromThisTask = 0
                        if obj.thisSteps == None:
                            obj.thisSteps = []
                            obj.save()
                        # it will check if (t) is in the thisSteps...
                        # that means somebody should click on done button to do_user this task...
                        #  not run run_user_task for this one
                        for itm in obj.thisSteps:
                            for itm2 in itm.keys():
                                if t.task_spec.name == itm[itm2]:
                                    flag3 = 1
                                    jumpFromThisTask = 1
                                    countHasJumped += 1
                                    if countHasJumped >= countTasks:
                                        enginefileClass = BpmsFileViewSet()
                                        enginefileClass = enginefileClass.updateEngineTempFile(obj.engineInstance,
                                                                                               pickle.dumps(self))
                                        return
                                    break
                            if jumpFromThisTask:
                                break
                        if not flag3:
                            # continue
                            if countHasRun < countTasks:
                                self.run_user_task(t, obj)
                                countHasRun += 1
                                if countHasRun >= countTasks:
                                    return
                            else:
                                return
                    elif type(t.task_spec) == NoneTaskSpecBpmn:
                        jumpFromThisTask = 0
                        self.run_message(t, obj, request)
                        obj.pastSteps.append(t.task_spec.name)
                        obj.save()
                        break
                    elif type(t.task_spec) == CallActivityBpmn:
                        jumpFromThisTask = 0
                        if countHasRun < countTasks:
                            t._state = 8
                            self.run_call_activity(t, obj, request)
                            countHasRun += 1
                            if countHasRun >= countTasks:
                                return
                        else:
                            return

                    if hasattr(t.task_spec, "cond_task_specs"):
                        jumpFromThisTask = 0
                        for cond, name in t.task_spec.cond_task_specs:
                            for cond_unit in cond.args:
                                if hasattr(cond_unit, "name"):
                                    condition_keys.append(cond_unit)
                    obj.pastSteps.append(t.task_spec.name)
                    obj.save()
                if SECURITYfor > 24:
                    return
            if not jumpFromThisTask:
                if not doneExactThisOne:
                    workflow.complete_next()
                else:
                    workflow.complete_task_from_id(doneExactThisOne)
                    workflow.last_task = doneExactThisOneTask
            if SECURITYfor > 24:
                return

            if SECURITYwhile > 12:
                return
        if workflow.is_completed():
            self.run_on_workflow_completed(obj, request)
        if SECURITYwhile > 24:
            return

    def keep_going_all_activity(self, taskId):
        """
            Usage of this function:
                it's gonna run when a child process has done
                 and parent workflow needs to go ahead
        """
        workflow = self.workflow
        tasks = workflow.get_tasks(Task.WAITING)
        for t in tasks:
            if t.task_spec.name == taskId:
                t._state = 16
                break
        workflow.complete_next()

    def _assign_selected_user(self, thisPerformers, userTask):
        """
            Usage of this function:
                it's gonna run when performer of current step is selected by bpmn designer

        """
        thisPerformers.append(str(userTask['performer']))
        return thisPerformers

    def _assign_selected_chart(self, thisPerformers, userTask):
        """
            Usage of this function:
                it's gonna run when performer of current step is selected by bpmn designer

        """
        chartId = int(userTask['chartPerformer'])
        positions = PositionsDocument.objects.filter(chartID=chartId)
        for itm in positions:
            thisPerformers.append(str(itm.id))
        return thisPerformers

    def _assign_selected_chart_name(self, thisPerformers, userTask, currPosId):
        """
            Usage of this function:
                it's gonna run when performer of current step is selected by bpmn designer

        """
        posObj = PositionsDocument.objects.get(id=ObjectId(currPosId))
        thisPerformers = {currPosId: posObj.profileName, 'avatar': posObj.avatar, 'chartTitle': posObj.chartName,
                          'id': str(posObj.id)}
        return thisPerformers

    def _assign_selected_user_name(self, thisPerformers, userTask, currPosId):
        """
            Usage of this function:
                it's gonna run when performer of current step is selected by bpmn designer

        """
        posObj = PositionsDocument.objects.get(id=str(userTask['performer']))
        thisPerformers = {currPosId: posObj.profileName, 'avatar': posObj.avatar, 'chartTitle': posObj.chartName,
                          'id': str(posObj.id)}
        return thisPerformers

    def _assign_process_starter(self, thisPerformers, obj):
        """
            Usage of this function:
                it's gonna run when performer of current step is starter of process

        """
        thisPerformers.append(str(obj.position_id))
        return thisPerformers

    def _assign_process_starter_name(self, thisPerformers, obj, currPosId):
        """
            Usage of this function:
                it's gonna run when performer of current step is starter of process

        """
        thisPerformers = {currPosId: obj.positionName, 'avatar': obj.positionPic, 'chartTitle': obj.chartTitle,
                          'id': currPosId}
        return thisPerformers

    def _assign_starter_boss(self, thisPerformers, obj):
        """
            Usage of this function:
                it's gonna run when performer of current step is boss of process's starter

        """
        allPositions = PositionsDocument.objects.all()
        allChart = Chart.objects.all()
        starterChartId = allPositions.get(id=ObjectId(obj.position_id)).chartID
        starterChart = allChart.get(id=int(starterChartId))
        # if users boss doesn't exist then this while is gonna
        # find boss of his boss and if again doesn't exist do same
        while True:
            topChart = allChart.filter(id=starterChart.top_id)
            if topChart.count != 0:  # found person :))
                topChart = topChart[0]
                foundPosition = PositionsDocument.objects.filter(chartID=topChart.id, userID__ne=None)
                if foundPosition.count != 0:
                    foundPosition = foundPosition.first()
                    if foundPosition.userID:  # it means if position has person in himself
                        thisPerformers.append(str(foundPosition.id))
                        return thisPerformers
                    if foundPosition.userID == None:
                        starterChart = Chart.objects.get(id=topChart.id)
                    if starterChart.top_id == None:
                        if topChart.userID == None:
                            thisPerformers.append(str(obj.position_id))
                            return thisPerformers  # when found no one return to starter
                            # when find boss loop ends chart and found no person to assign
                            # raise Exception("1#All personel has no user iD , check chart design")
            else:
                thisPerformers.append(str(obj.position_id))
                return thisPerformers  # when found no one return to starter
                # raise Exception("2#All personel has no user iD , check chart design")

        # while allPositions.filter(chartID=starterChart.top_id).count() == 0:
        #     starterChart = allChart.get(id=starterChart.top_id)
        #     if starterChart.top_id == None:
        #         thisPerformers.append(str(obj.position_id))
        #         return thisPerformers
        # thisPerformers.append(str(allPositions.filter(chartID=starterChart.top_id)[0].id))
        # return thisPerformers

    def _assign_starter_boss_rank(self, thisPerformers, obj, currentTask):
        """
            Usage of this function:
                it's gonna run when performer of current step is boss of process's starter and get to top of
                them by rank

        """
        allPositions = PositionsDocument.objects.filter(userID__ne=None)
        allChart = Chart.objects.all()
        starterChartId = allPositions.get(id=ObjectId(obj.position_id)).chartID
        starterChart = allChart.get(id=int(starterChartId))

        # if users boss doesn't exist then this while is gonna
        # find boss of his boss and if again doesn't exist do same
        # if it could not find the boss it forward the job for starter

        thisPerformers = []
        found = False
        currentChart = None
        while not found:
            if not currentChart:
                currentChart = allChart.get(id=starterChart.id)

            if currentChart.rank == currentTask.get("chartRank"):
                thisPerformers.append(str(allPositions.filter(chartID=currentChart.id, userID__ne=None).first().id))
                found = True
            else:
                currentChart = allChart.get(id=currentChart.top_id)

            if currentChart.top_id == None and len(thisPerformers) == 0:  # when rank does not found it goes to CEO
                thisPerformers.append(str(obj.position_id))
                found = True

            # pass

        # thisPerformers.append(str(allPositions.filter(chartID=starterChart.top_id)[0].id))
        return thisPerformers

    def _assign_starter_boss_name(self, thisPerformers, obj, currPosId):
        """
            Usage of this function:
                it's gonna run when performer of current step is boss of process's starter

        """
        allPositions = PositionsDocument.objects.all()
        allChart = Chart.objects.all()
        starterChartId = allPositions.get(id=ObjectId(obj.position_id)).chartID
        starterChart = allChart.get(id=int(starterChartId))
        # if users boss doesn't exist then this while is gonna
        # find boss of his boss and if again doesn't exist do same
        while allPositions.filter(chartID=starterChart.top_id).count() == 0:
            starterChart = allChart.get(id=starterChart.top_id)
            if starterChart.top_id == None:
                thisPerformers = {currPosId: obj.positionName, 'avatar': obj.positionPic,
                                  'chartTitle': starterChart.title, 'id': currPosId}
                return thisPerformers
        posObj = allPositions.filter(chartID=starterChart.top_id)[0]
        thisPerformers = {currPosId: posObj.profileName, 'avatar': posObj.avatar, 'chartTitle': posObj.chartName,
                          'id': str(posObj.id)}
        return thisPerformers

    def _assign_starter_boss_name_by_rank(self, thisPerformers, obj, currPosId, currentTask):
        """
            Usage of this function:
                it's gonna run when performer of current step is boss of process's starter

        """
        allPositions = PositionsDocument.objects.all()
        allChart = Chart.objects.all()
        starterChartId = allPositions.get(id=ObjectId(obj.position_id)).chartID
        starterChart = allChart.get(id=int(starterChartId))
        # if users boss doesn't exist then this while is gonna
        # find boss of his boss and if again doesn't exist do same
        thisPerformers = []
        found = False
        currentChart = None
        while not found:
            if not currentChart:
                currentChart = allChart.get(id=starterChart.id)

            if currentChart.rank == currentTask.get("chartRank"):
                thisPerformers.append(str(allPositions.filter(chartID=currentChart.id).first().id))
                found = True
            else:
                currentChart = allChart.get(id=currentChart.top_id)

            if currentChart.top_id == None and len(thisPerformers) == 0:  # when rank does not found it goes to CEO
                thisPerformers.append(str(obj.position_id))
                found = True

        posObj = allPositions.get(id=thisPerformers[0])

        thisPerformers = {currPosId: posObj.profileName,
                          'avatar': posObj.avatar,
                          'chartTitle': posObj.chartName,
                          'id': str(posObj.id)}
        return thisPerformers

    def _assign_form_selected_user(self, thisPerformers, obj, userTask):
        """
            Usage of this function:
                it's gonna run when performer type of current step is form type
                that means the performer of current step was entered in previous steps

        """
        thisPerformers = [obj.formData[userTask['performer']]]
        return thisPerformers

    def _assign_form_selected_user_name(self, thisPerformers, obj, userTask, currPosId):
        """
            Usage of this function:
                it's gonna run when performer type of current step is form type
                that means the performer of current step was entered in previous steps

        """
        posObj = PositionsDocument.objects.get(id=obj.formData[userTask['performer']])
        thisPerformers = {currPosId: posObj.profileName, 'avatar': posObj.avatar,
                          'chartTitle': posObj.chartName, 'id': str(posObj.id)}
        return thisPerformers
