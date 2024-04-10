from amspApp.BI.DataTables.models import DataTable, TemporaryDataTableValuesForProcess
from amspApp.BI.DataTables.serializers.DataTableValuesSerializer import DataTableValuesSerializer
from amspApp.CompaniesManagment.PythonCodeRunner.PythonRunner import PythonRunner
from amspApp.ControlProject.serializers.ControlProjectYearsSerializer import ControlProjectYearsSerializer


from amspApp.Infrustructures.Classes.DateConvertors import sh_to_mil
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class ServiceTaskLauncher():
    currentPerformerPositionInstance = None
    currentStep = None
    lunchedProcessInstance = None
    taskObject = None

    def __init__(self, currentPerformerPositionInstance, currentStep, LunchedProcessInstance, TaskObject, request):

        self.currentPerformerPositionInstance = currentPerformerPositionInstance
        self.currentStep = currentStep
        self.lunchedProcessInstance = LunchedProcessInstance
        self.taskObject = TaskObject
        self.request = request
        self.currentTask = None
        self.form = self.lunchedProcessInstance.formData
        self.user = request.user
        self.currentCompany = request.user.current_company
        self.currentPos = GetPositionViewset().GetCurrentPositionDocumentInstance(request)

        for service in self.lunchedProcessInstance.bpmn['otherTasks']:
            if service['taskId'] == TaskObject.task_spec.name:
                self.currentTask = service

    def do(self):
        # handling just one time run
        # this problem cause parallel gatway loop execute more than one !
        if not self.currentTask.get('pythonCodeDone'):
            PythonRunner().runServiceTaskPython(self, self.currentTask['pythonCode'])
        self.currentTask['pythonCodeDone'] = True

    def addNewProject(self, title, startDate, endDate):
        dt = dict(
            startDate=sh_to_mil(startDate, ResultSplitter="-") + "T00:01",
            endDate=sh_to_mil(endDate, ResultSplitter="-") + "T23:59",
            positionID=self.currentPos.positionID,
            companyID=self.currentCompany.id,
            title=title
        )

        ser = ControlProjectYearsSerializer(data=dt)
        ser.is_valid(raise_exception=True)
        ser.save()
        print("new control project year saved ...")
        return ser.data

    def updateStorage(self, keyName, value):
        currentDict = self.lunchedProcessInstance.bpmn.get('storage')
        if not currentDict:
            currentDict = {}
        currentDict[keyName] = value
        self.lunchedProcessInstance.update(set__bpmn__storage=currentDict)
        return self.lunchedProcessInstance.bpmn['storage']

    def addTmpDataTableToDataTable(self, tmpDataTableObjName):
        # ------------------------------------
        # ------------------------------------
        # finding datatable ID
        dataTableID = None
        for form in self.lunchedProcessInstance.bpmn["form"]:
            for field in form["schema"]["fields"]:
                if field["name"] == tmpDataTableObjName:
                    dataTableID = field["datatable"]
        dataTableInstance = DataTable.objects.get(id=dataTableID)
        # ------------------------------------
        # ------------------------------------
        # ------------------------------------
        # getting tmpDataTableInstance
        tmps = TemporaryDataTableValuesForProcess.objects.filter(dataTableLink=dataTableInstance.id,
                                                                 launchedProcessID=self.lunchedProcessInstance.id)

        tmps = tmps.first()
        if tmps:
            for t in tmps.values:
                dt = {
                    'position_id': self.currentPos.positionID,
                    'companyId': self.currentPos.companyID,
                    'values': t,
                    'dataTableLink': dataTableInstance.id,
                }
                serial = DataTableValuesSerializer(data=dt)
                serial.is_valid(raise_exception=True)
                serial.save()
