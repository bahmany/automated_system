from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.PythonCodeRunner.PythonRunner import PythonRunner
from amspApp.amspUser.models import MyUser


class DataTablePythonScriptRunner:
    def __init__(self, dataTableInstance):
        self.dataTableInstance = dataTableInstance
        self.dataTableCreatorPositionInstance = PositionsDocument.objects.filter(
            positionID=self.dataTableInstance.position_id).first()
        self.valueInsertPositionInstance = PositionsDocument.objects.filter(
            positionID=self.dataTableInstance.position_id).first()

    def doBeforeInsert(self, pythonCode, dataBeforeSave):
        if not pythonCode:
            return
        self.dataBeforeSave = dataBeforeSave
        PythonRunner().runDataTableValuePython(self, pythonCode)

    def doAfterInsert(self, pythonCode, dataAfterSave):
        if not pythonCode:
            return
        self.dataAfterSave = dataAfterSave
        PythonRunner().runDataTableValuePython(self, pythonCode)

    def getDataFromValues(self, dataTableValueInstance, key):
        for v in dataTableValueInstance.values:
            if v['uid'] == key:
                if v['dataType'] == "int":
                    return int(v.get("value"))
                return v.get("value")

    def runProcess(self, bpmnID, performerPositionID):
        # creating process instance
        # {'name': 'dfsdfsd', 'bpmnForCreate': '5a6c677f2bb07d06046c0c90'}
        # preparing fake request for running view
        class Object(object):
            pass

        request = Object()
        performerPositionInstance = PositionsDocument.objects.filter(positionID=performerPositionID).first()
        userInstance = MyUser.objects.get(id=performerPositionInstance.userID)
        request.user = userInstance
        request.data = {
            "name": "توسط جدول داده ها",
            "bpmnForCreate": bpmnID}
        from amspApp.BPMSystem.views.LunchedProcessView import LunchedProcessViewSet
        vw = LunchedProcessViewSet()
        result = vw.create(request)

        form = vw.retrieve(request, id=result.data.get("id"))
        for k in self.mapping.keys():
            self.mapping[k] = self.getDataFromValues(self.dataAfterSave, self.mapping[k])
        finalFormToSend = {}
        finalFormToSend["formSchema"] = form.data["formSchema"]
        finalFormToSend["formData"] = self.mapping
        finalFormToSend["taskID"] = form.data['curAndPrevSteps']['taskId']
        new_request = request
        new_request.data = finalFormToSend
        # new view
        vw = LunchedProcessViewSet(kwargs={"id": result.data['id']})
        result = vw.CompleteJob(new_request, id=result.data['id'])

        return result
