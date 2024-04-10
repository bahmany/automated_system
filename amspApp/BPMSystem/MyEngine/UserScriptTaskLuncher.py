from amspApp.CompaniesManagment.PythonCodeRunner.PythonRunner import PythonRunner
from amspApp.ControlProject.serializers.ControlProjectYearsSerializer import ControlProjectYearsSerializer
from amspApp.Infrustructures.Classes.DateConvertors import sh_to_mil
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class UserTaskScriptLauncher():
    currentPerformerPositionInstance = None
    currentStep = None
    lunchedProcessInstance = None
    taskObject = None

    def __init__(self, this, currentStep, LunchedProcessInstance, currentTask):
        self.this = this
        self.currentStep = currentStep
        self.lunchedProcessInstance = LunchedProcessInstance
        self.request = this.request
        self.positionInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(self.request)
        self.currentTask = currentTask


    def do(self, pyCode):
        # handling just one time run
        # this problem cause parallel gatway loop execute more than one !
        if not self.currentTask.get('pythonCodeDone'):
            PythonRunner().runPythonFromUserTask(self, pyCode)
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
        self.lunchedProcessInstance.update(set__bpmn__storage = currentDict)
        return self.lunchedProcessInstance.bpmn['storage']


