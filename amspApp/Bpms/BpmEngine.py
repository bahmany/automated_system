# -*- coding: utf-8
import io
import os
import pickle
import sys
from copy import copy
from datetime import datetime

from bson import ObjectId

from amspApp.Bpms.MyPackager import MyPackager
from amspApp.CompaniesManagment.Charts.models import Chart
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.FileServer.views.BpmsFileView import BpmsFileViewSet
from amspApp.Infrustructures.MySpiffWorkflow.bpmn.BpmnWorkflow import BpmnWorkflow

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../lib'))

from amspApp.Infrustructures.MySpiffWorkflow import Task

from amspApp.Infrustructures.MySpiffWorkflow.bpmn.storage.BpmnSerializer import BpmnSerializer
from amspApp.Infrustructures.MySpiffWorkflow.specs.StartTask import StartTask as StartTaskREAL
from amspApp.Infrustructures.MySpiffWorkflow.bpmn.specs.UserTask import UserTask as UserTaskSpecBpmn
from amspApp.Infrustructures.MySpiffWorkflow.bpmn.specs.EndEvent import EndEvent as EndEventSpecBpmn
from amspApp.Infrustructures.MySpiffWorkflow.bpmn.specs.NoneTask import NoneTask as NoneTaskSpecBpmn
from amspApp.Bpms.models import LunchedProcess, LunchedProcessArchive, DoneProcessArchive, LunchedProcessMessages, \
    Statistic


class BpmEngine(object):
    def __init__(self, xml, forms, userTasks, taskObjId):
        self.serializer = BpmnSerializer()
        self.package = io.BytesIO()
        self.forms = forms
        self.taskObjId = taskObjId
        self.userTasks = userTasks
        package = MyPackager(self.package, 'Process_1')
        self.xml = xml
        package.add_bpmn_file(self.xml)
        package.create_package_xml()
        self.wf_spec = self.serializer.deserialize_workflow_spec(self.package)
        # self.taken_path = self.track_workflow(self.wf_spec)
        self.workflow = BpmnWorkflow(self.wf_spec)


    def setThisPerformers(self, obj, ut):
        ut['performerType'] = int(ut['performerType'])
        if ut['performerType'] == 1:
            obj.thisPerformers = []
            obj.thisChartPerformer = ut['chartPerformer']
            obj.thisPerformers.append(str(ut['performer']))
        if ut['performerType'] == 3:
            obj.thisPerformers = []
            obj.thisPerformers.append(str(obj.position_id))
        if ut['performerType'] == 5:
            obj.thisPerformers = []
            allPositions = PositionsDocument.objects.all()
            allChart = Chart.objects.all()
            starterChartId = allPositions.get(id=ObjectId(obj.position_id)).chartID
            starterChart = allChart.get(id=int(starterChartId))
            while allPositions.filter(chartID=starterChart.top_id).count() == 0:
                starterChart = allChart.get(id=starterChart.top_id)
                if starterChart.top_id == None:
                    obj.thisPerformers.append(str(obj.position_id))
                    return obj
            obj.thisPerformers.append(str(allPositions.filter(chartID=starterChart.top_id)[0].id))
        if ut['performerType'] == 6:
            obj.thisPerformers = []
            obj.thisPerformers = [obj.formData[ut['performer']]]

        return obj

    def getPerformerForMessage(self, obj, ut):
        thisPerformers = []
        ut['performerType'] = int(ut['performerType'])
        if ut['performerType'] == 1:
            thisPerformers = []
            thisPerformers.append(str(ut['performer']))
        if ut['performerType'] == 3:
            thisPerformers = []
            thisPerformers.append(str(obj.position_id))
        if ut['performerType'] == 5:
            thisPerformers = []
            allPositions = PositionsDocument.objects.all()
            allChart = Chart.objects.all()
            starterChartId = allPositions.get(id=ObjectId(obj.position_id)).chartID
            starterChart = allChart.get(id=int(starterChartId))
            while allPositions.filter(chartID=starterChart.top_id).count() == 0:
                starterChart = allChart.get(id=starterChart.top_id)
                if starterChart.top_id == None:
                    thisPerformers.append(str(obj.position_id))
                    return obj
            thisPerformers.append(str(allPositions.filter(chartID=starterChart.top_id)[0].id))
        if ut['performerType'] == 6:
            thisPerformers = []
            thisPerformers = [obj.formData[ut['performer']]]
        return thisPerformers

    def run(self):
        workflow = self.workflow
        condition_keys = []
        while not workflow.is_completed():
            tasks = workflow.get_tasks(Task.READY)
            for t in tasks:
                obj = LunchedProcess.objects.get(pk=self.taskObjId)
                amir = copy(obj.formData)
                t.set_data(**amir)
                if type(t.task_spec) == UserTaskSpecBpmn:
                    for ut in self.userTasks:
                        if ut['taskId'] == t.task_spec.name:
                            obj.performerType = ut['performerType']
                            obj = self.setThisPerformers(obj, ut)
                            obj.thisStep = ut['taskId']
                            obj.save()
                            enginefileClass = BpmsFileViewSet()
                            enginefileClass = enginefileClass.updateEngineTempFile(obj.engineInstance,
                                                                                   pickle.dumps(self))
                            for itm2 in obj.thisPerformers:
                                # currentPosition = PositionsDocument.objects.get(userID=request.user.id,
                                # companyID=request.user.current_company.id)
                                try:
                                    counterObj = Statistic.objects.get(position_id=ObjectId(itm2))
                                except:
                                    counterObj = Statistic(position_id=ObjectId(itm2))
                                counterObj.Lp += 1
                                counterObj.newLp += 1
                                counterObj.save()
                    return

                if hasattr(t.task_spec, "cond_task_specs"):
                    for cond, name in t.task_spec.cond_task_specs:
                        for cond_unit in cond.args:
                            if hasattr(cond_unit, "name"):
                                condition_keys.append(cond_unit.name)

                                # for t in tasks:
                                # t.set_data(**self.userTasks)
                obj.pastSteps.append(t.task_spec.name)
                if type(t.task_spec) != StartTaskREAL:
                    for itm in t.task_spec.outgoing_sequence_flows_by_id.keys():
                        obj.pastSteps.append(itm)

                obj.save()
            workflow.complete_next()

    def keep_going(self, request=None, databaseData=None):
        workflow = self.workflow
        condition_keys = []
        while not workflow.is_completed():
            tasks = workflow.get_tasks(Task.READY)
            # waitingTasks = workflow.get_tasks(Task.WAITING)
            obj = LunchedProcess.objects.get(pk=self.taskObjId)

            for t in tasks:
                amir = copy(obj.formData)
                if not amir == None:
                    t.set_data(**amir)

                if not obj.thisStep == t.task_spec.name:
                    if type(t.task_spec) == EndEventSpecBpmn:
                        currentPosition = PositionsDocument.objects.get(companyID=request.user.current_company.id,
                                                                        userID=request.user.id)
                        archiveObjs = LunchedProcessArchive.objects.filter(lunchedProcessId=obj.id)
                        for itm in archiveObjs:
                            new = DoneProcessArchive(
                                user_id=itm.user_id,
                                position_id=itm.position_id,
                                positionName=itm.positionName,
                                bpmn=itm.bpmn,
                                name=itm.name,
                                stepsWithDates=itm.stepsWithDates,
                                performer=itm.performer,
                                chartPerformer=itm.chartPerformer,
                                pastSteps=itm.pastSteps.pastSteps,
                                steps=itm.steps,
                                engineInstance=itm.engineInstance,
                                formData=itm.formData,
                                startProcessDate=itm.startProcessDate,
                                postDate=datetime.now()
                            )
                            new.pastSteps.append(t.task_spec.name)
                            new.save()
                            itm.delete()
                        obj.delete()

                    if type(t.task_spec) == UserTaskSpecBpmn:
                        for ut in self.userTasks:
                            if ut['taskId'] == t.task_spec.name:
                                obj = self.setThisPerformers(obj, ut)
                                obj.thisStep = ut['taskId']
                                enginefileClass = BpmsFileViewSet()
                                obj.engineInstance = enginefileClass.updateEngineTempFile(obj.engineInstance,
                                                                                          pickle.dumps(self))

                                for itm1 in obj.thisPerformers:
                                    try:
                                        counterObj = Statistic.objects.get(position_id=ObjectId(itm1))
                                    except:
                                        counterObj = Statistic(position_id=ObjectId(itm1))
                                    counterObj.Lp += 1
                                    counterObj.newLp += 1
                                    counterObj.save()
                                    obj.save()
                        return
                    if type(t.task_spec) == NoneTaskSpecBpmn:
                        for ut in self.userTasks:
                            if ut['taskId'] == t.task_spec.name:
                                currentPosition = PositionsDocument.objects.get(
                                    companyID=request.user.current_company.id,
                                    userID=request.user.id)
                                new = LunchedProcessMessages(
                                    user_id=obj.user_id,
                                    position_id=obj.position_id,
                                    lunchedProcessId=obj.id,
                                    positionName=obj.positionName,
                                    bpmn=obj.bpmn,
                                    bpmnForCreate=obj.bpmnForCreate,
                                    name=obj.name,
                                    thisStep=t.task_spec.name,
                                    thisPerformers=self.setThisPerformers(obj, ut).thisPerformers,
                                    previousPerformer={'id': currentPosition.id,
                                                       'profileName': currentPosition.profileName},
                                    pastSteps=obj.pastSteps,
                                    engineInstance=obj.engineInstance,
                                    formData=obj.formData,
                                    hasApprove=False,
                                    hasApproveMainId=obj.id,
                                    postDate=obj.postDate,
                                    lastInboxChangeDate=datetime.now()
                                )
                                new.save()

                                reciversOfMessage = self.getPerformerForMessage(obj, ut)
                                for rc in reciversOfMessage:
                                    archiveObjects = LunchedProcessArchive.objects.filter(lunchedProcessId=obj.id,
                                                                                          performer=rc)
                                    try:
                                        counterObj = Statistic.objects.get(position_id=ObjectId(rc))
                                    except:
                                        counterObj = Statistic(position_id=ObjectId(rc))
                                    counterObj.Mp+=1
                                    counterObj.newMp+=1
                                    counterObj.save()
                                    if archiveObjects.count() == 0:
                                        stepsWithDates = {}
                                        stepsWithDates[obj.thisStep] = {"comeToInbox": obj.lastInboxChangeDate,
                                                                        "done": datetime.now()}
                                        new2 = LunchedProcessArchive(
                                            user_id=obj.user_id,
                                            position_id=obj.position_id,
                                            positionName=obj.positionName,
                                            lunchedProcessId=obj.id,
                                            bpmn=obj.bpmn,
                                            name=obj.name,
                                            stepsWithDates=stepsWithDates,
                                            performer=rc,
                                            chartPerformer=currentPosition.chartID,
                                            pastSteps=obj.id,
                                            steps=[t.task_spec.name],
                                            engineInstance=obj.engineInstance,
                                            formData=obj.formData,
                                            startProcessDate=obj.postDate,
                                        )

                                        new2.save()
                                    else:
                                        objForUpdate = archiveObjects[0]
                                        stepsWithDates = objForUpdate.stepsWithDates
                                        stepsWithDates[obj.thisStep] = {"comeToInbox": obj.lastInboxChangeDate,
                                                                        "done": datetime.now()}
                                        objForUpdate.formData = obj.formData
                                        objForUpdate.stepsWithDates = stepsWithDates
                                        objForUpdate.steps.append(obj.thisStep)
                                        objForUpdate.steps.append(t.task_spec.name)
                                        objForUpdate.save()

                # it will run when user would click on done
                else:
                    if type(t.task_spec) == UserTaskSpecBpmn:
                        currentPosition = PositionsDocument.objects.get(companyID=request.user.current_company.id,
                                                                        userID=request.user.id)
                        for itm3 in obj.thisPerformers:
                            try:
                                counterObj = Statistic.objects.get(position_id=ObjectId(itm3))
                            except:
                                counterObj = Statistic(position_id=ObjectId(itm3))
                            counterObj.Lp-=1
                            # counterObj.newLp+=1
                            counterObj.save()

                        if str(currentPosition.id) in obj.thisPerformers:
                            archiveObjects = LunchedProcessArchive.objects.filter(lunchedProcessId=obj.id,
                                                                                  performer=currentPosition.id)
                            if archiveObjects.count() == 0:
                                stepsWithDates = {}
                                stepsWithDates[obj.thisStep] = {"comeToInbox": obj.lastInboxChangeDate,
                                                                "done": datetime.now()}
                                new = LunchedProcessArchive(
                                    user_id=obj.user_id,
                                    position_id=obj.position_id,
                                    positionName=obj.positionName,
                                    lunchedProcessId=obj.id,
                                    bpmn=obj.bpmn,
                                    name=obj.name,
                                    stepsWithDates=stepsWithDates,
                                    performer=currentPosition.id,
                                    chartPerformer=currentPosition.chartID,
                                    pastSteps=obj.id,
                                    steps=[obj.thisStep],
                                    engineInstance=obj.engineInstance,
                                    formData=obj.formData,
                                    startProcessDate=obj.postDate,
                                )
                                obj.lastInboxChangeDate = datetime.now()
                                obj.save()
                                new.save()
                            else:
                                objForUpdate = archiveObjects[0]
                                stepsWithDates = objForUpdate.stepsWithDates
                                stepsWithDates[obj.thisStep] = {"comeToInbox": obj.lastInboxChangeDate,
                                                                "done": datetime.now()}
                                objForUpdate.formData = obj.formData
                                objForUpdate.stepsWithDates = stepsWithDates
                                objForUpdate.steps.append(obj.thisStep)
                                objForUpdate.save()
                                obj.lastInboxChangeDate = datetime.now()
                                obj.save()
                        else:
                            return 'erorrrrrr'
                if hasattr(t.task_spec, "cond_task_specs"):
                    for cond, name in t.task_spec.cond_task_specs:
                        for cond_unit in cond.args:
                            if hasattr(cond_unit, "name"):
                                condition_keys.append(cond_unit)
                obj.pastSteps.append(t.task_spec.name)
                obj.save()

            workflow.complete_next()
