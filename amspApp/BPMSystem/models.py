from datetime import datetime

from mongoengine import *

from amspApp.BI.DataTables.models import DataTable, DataTableValues
from amspApp.CompaniesManagment.Connections.models import Connections, ConnectionPools




class LunchedProcess(Document):
    """
    position_id:
        owner (starter) of this process
    =======================
    positionName:
        owner (starter) of this process

    ====================
    postDate :
        it's the time that this object created (time of start process)

    ===================
    lastInboxChangeDate:
        the time that process was transfer to thisPerformer inbox (time of come to new performer's inbox)

    ===============
    bpmnForCreate
        it's the name of your selected bpmn instance

    ===============
    name
        it's a name that your entered for your lunched process's name

    ===============
    bpmn
        bpmn object


    ===============
    be aware, you should show performers their steps using this field
    thisSteps
        current steps whit performers :
        [{'CURRENT_PERFORMER_ID':'CURRENT_STEP'},
        {'CURRENT_PERFORMER_ID':'CURRENT_STEP'},
            .............
        ]

    ===============

    thisStepsNames
        current steps whit performers :
        [{'CURRENT_PERFORMER_ID':'CURRENT_STEP_NAME'},
        {'CURRENT_PERFORMER_ID':'CURRENT_STEP_NAME'},
            .............
        ]

    ===============
    thisPerformers
        List of current performers of this process

    =============================================
    it's performer type only for current step and current performer
    performerType:
        1 --> position
        2 --> chart(automatic select the most free person)
        3 --> starter
        4 --> group
        5 --> boss
        6 --> choose in previous step
        7 --> list of persons...
        ...

    ===============================
    thisChartPerformer
        the chart of current performer

    ===============================
    allPerformers
        list of all performers of this process

    ===============================
    pastSteps
        The steps were done in past

    ===============================
    engineInstance
        The address of the file that contains binary data of engine class

    ===============================
    formData
        The data was entered in previous steps

    ===============================
    previousPerformer
        The previous performer :
        [{'CURRENT_PERFORMER_ID':{'id':'POSITION ID','name':'PROFILE NAME','avtar':'IMAGE'},
         {'CURRENT_PERFORMER_ID':{'id':'POSITION ID','name':'PROFILE NAME','avtar':'IMAGE'},
        ...
        ]
    ==================
    positionName
        creators name

    ==================
    seen
       [{'CURRENT_PERFORMER_ID':0/1},
        {'CURRENT_PERFORMER_ID':0/1},
        ...
        ]

    ==================
    isHide
        maybe it'll be useful
    """

    user_id = IntField()
    position_id = ObjectIdField()
    positionName = StringField(null=True, required=False)
    chartTitle = StringField(null=True, required=False)
    chartId = IntField(null=True, required=False)
    positionPic = StringField(null=True, required=False)
    bpmn = DictField(null=True, required=False)
    bpmnForCreate = StringField(max_length=255, null=True, required=False)
    name = StringField(max_length=255, null=True, required=False)
    thisSteps = ListField(required=False, default=[], null=True)
    thisPerformers = ListField(required=False, default=[])
    PrevPerformersDetail = ListField(required=False, default=[])
    StepHistory = ListField(required=False, default=[])
    allPerformers = ListField(required=False, default=[])
    thisPerformerType = ListField(default=[])
    thisChartPerformer = ListField(default=[])
    thisChartList = ListField(default=[])
    thisStepsNames = ListField(required=False, default=[])
    pastSteps = ListField(required=False, default=[])
    engineInstance = StringField(null=True, required=False)
    seen = ListField(default=[])
    formData = DictField(null=True, required=False)
    subProcess = DictField(null=True, required=False)
    postDate = DateTimeField(
        default=datetime.now,
        required=False,
        null=True
    )
    lastInboxChangeDate = ListField(default=[])
    isHide = BooleanField(default=False)
    parentId = ObjectIdField(null=True, required=False)
    parentBpmnName = StringField(null=True, required=False)
    parentTaskId = StringField(null=True, required=False)
    childId = ListField(default=[])


"""
scenario :
first we have to say what is suppose to dedicate by this model
it will create when performer of this step approve its user task
here we are suppose to split finnished and unfinnished process
when process in not finished or in lunched mode, "isFinished = Fasle"
when process in done ( done process = finished process ) , "isFinished = True" and it will update all rows
so we can split done and lunched processes with isFinished key

"""


class BigArchive(Document):
    bpmnName = StringField(null=True, required=False)
    bpmnId = ObjectIdField(null=True, required=False)
    processId = ObjectIdField(null=True, required=False)
    companyId = IntField(null=True, required=False)
    taskId = StringField(null=True, required=False)
    taskName = StringField(null=True, required=False)
    startDate = DateTimeField(null=True, required=False)
    postDate = DateTimeField(null=True, required=False)
    doneDate = DateTimeField(null=True, required=False)
    BAMHours = FloatField(null=True, required=False, default=-1)
    BAMDate = DateTimeField(null=True, required=False)
    prevPerformer = DictField(null=True, required=False)
    StepHistory = ListField(required=False, default=[])
    prevStepName = StringField(null=True, required=False)
    starterId = ObjectIdField(null=True, required=False)
    starterName = StringField(null=True, required=False)
    starterChartName = StringField(null=True, required=False)
    thisPerformerId = ObjectIdField(null=True, required=False)
    thisPerformerName = StringField(null=True, required=False)
    thisPerformerAvatar = StringField(null=True, required=False)
    thisPerformerChartName = StringField(null=True, required=False)
    thisPerformerChartId = IntField(null=True, required=False)
    isStepDone = BooleanField(default=False)
    isProcessDone = BooleanField(default=False)
    isChild = BooleanField(null=True, required=False)
    parentProcessId = ObjectIdField(null=True, required=False)
    parentProcessName = StringField(null=True, required=False)
    childProcessId = ListField(null=True, required=False)
    thisForm = ListField(null=True, required=False, default=[])
    extra = DictField(null=True, required=False, default={})


class LunchedProcessMessages(Document):
    """
    position_id:
        owner (starter) of this process

    ====================
    postDate :
        it's the time that this object created (time of start process)

    ===================
    lastInboxChangeDate:
        the time that process was transfer to thisPerformer inbox (time of come to new performer's inbox)

    ===============
    bpmnForCreate
        it's the name of your selected bpmn instance

    ===============
    name
        it's a name that your entered for your lunched process's name

    ===============
    bpmn
        bpmn object

    ===============
    thisStep
        current step of this process

    ===============
    thisDesc
        current step of this process description

    ===============
    thisPerformer
        List of current performers of this process

    =============================================
    it's performer type only for current step and current performer
    performerType:
        1 --> position
        2 --> chart(automatic select the most free person)
        3 --> starter
        4 --> group
        5 --> boss
        6 --> choose in previous step
        7 --> list of persons...
        ...

    ===============================
    thisChartPerformer
        the chart of current performer

    ===============================
    pastSteps
        The steps were done in pas

    ===============================
    engineInstance
        The address of the file that contains binary data of engine class

    ===============================
    formData
        The data was entered in previous steps

    ===============================
    previousPerformer
        The previous performer :
        {'id':'POSITION ID','name':'PROFILE NAME'}

    ===============================
    allPerformers
        list of all performers of this process

    """

    user_id = IntField()
    positionName = StringField(required=False, null=True)
    positionPic = StringField(required=False, null=True)
    chartTitle = StringField(required=False, null=True)
    chartId = StringField(required=False, null=True)
    position_id = ObjectIdField(required=False, null=True)
    lunchedProcessId = ObjectIdField(required=False, null=True)
    bpmn = DictField(null=True, required=False)
    bpmnForCreate = StringField(max_length=255, null=True, required=False)
    name = StringField(max_length=255, null=True, required=False)
    thisStep = StringField(max_length=255, null=True, required=False)
    thisStepName = StringField(max_length=255, null=True, required=False)
    prevStep = StringField(max_length=255, null=True, required=False)
    prevStepName = StringField(max_length=255, null=True, required=False)
    thisDesc = StringField(max_length=755, null=True, required=False)  # added by MRB 02/09/1394
    thisPerformer = ObjectIdField(required=False, null=True)
    performerDetail = DictField(required=False, null=True, default={})
    prevPerformer = DictField(required=False, null=True, default={})
    pastSteps = ListField(required=False, default=[])
    startProcessDate = DateTimeField(null=True, required=False)
    formData = DictField(null=True, required=False)
    seen = BooleanField(default=False)
    postDate = DateTimeField(
        default=datetime.now,
        required=False,
        null=True
    )
    lastInboxChangeDate = DateTimeField(
        default=datetime.now,
        required=False,
        null=True
    )


class LunchedProcessArchive(Document):
    """
    position_id:
        owner (starter) of this process

    ====================
    stepsWithDates :
        A dict that contains steps(which you have approve them) with
         their comeToInbox and done date, like this:
        {'STEP NAME':{'comeToInbox':"THE DATE", 'done':"THE DATE"},
         'STEP NAME':{'comeToInbox':"THE DATE", 'done':"THE DATE"},
             ...
        }

    ===============
    bpmn
        bpmn object

    ===============
    steps
        A list that contains steps which you have done them

    ===============
    performer_id
        PositionId of performer who has done these steps

    ===============================
    chartPerformer
        ChartId of performer who has done these steps

    ===============================
    pastSteps
        ReferenceField to LunchedProcess in order to get latest pastSteps

    ===============================
    engineInstance
        The address of the file that contains binary data of engine class

    ===============================
    formData
        The data was entered in previous steps

    ===============================
    lunchedProcessId
        Id of lunched process it will be useful when i want to check
        is there any archive object for this lunched process and
        performer or not

    ===============================
    previousPerformer
        The previous performer :
        {'id':'POSITION ID','name':'PROFILE NAME','STEP ID'}

    ===============================
    allPerformers
        list of all performers of this process


    """

    user_id = IntField()
    position_id = ObjectIdField()
    positionName = StringField()
    chartTitle = StringField()
    positionPic = StringField(null=True, required=False)
    lastUrStepName = StringField(null=True, required=False)
    lastUrPrevPerformerName = StringField(null=True, required=False)
    bpmnName = StringField(null=True, required=False)
    chartId = IntField()
    lunchedProcessId = ObjectIdField(null=True, required=False, default={})
    bpmn = DictField()
    name = StringField()
    stepsWithDates = DictField(null=True, required=False, default={})
    performer = ObjectIdField()
    chartPerformer = StringField(null=True, required=False)
    prevPerformer = DictField(null=True, required=False)
    pastSteps = ObjectIdField()
    steps = ListField(null=True, required=False, default=[])
    formData = DictField(null=True, required=False)
    startProcessDate = DateTimeField(default=datetime.now, required=False, null=True)
    postDate = DateTimeField(default=datetime.now, required=False, null=True)
    isHide = BooleanField(default=False)


class DoneProcessArchive(Document):
    """
    position_id:
        owner (starter) of this process

    ====================
    stepsWithDates :
        A dict that contains steps(which you have approve them) with their comeToInbox and done date, like this:
        {'STEP NAME':{'comeToInbox':"THE DATE", 'done':"THE DATE"},
         'STEP NAME':{'comeToInbox':"THE DATE", 'done':"THE DATE"},
             ...
        }

    ===============
    bpmnForCreate
        it's a name that owner was entered when create lunch process

    ===============
    bpmn
        bpmn object

    ===============
    steps
        A list that contains steps(which you have approve them)

    ===============
    performer
        PositionId of performer who have approve these steps

    ===============================
    chartPerformer
        ChartId of performer who have approve these steps

    ===============================
    pastSteps
        List of done steps

    ===============================
    engineInstance
        The address of the file that contains binary data of engine class

    ===============================
    formData
        The data was entered in previous steps

    ===============================
    postDate
        Time of object creation (when the process was done)

    ===============================
    lunchedProcessId
        Id of lunched process it will be useful when i want to check
        delete...

    ===============================
    allPerformers
        list of all performers of this process

    """

    user_id = IntField()
    position_id = ObjectIdField()
    positionName = StringField()
    positionPic = StringField()
    chartTitle = StringField()
    lastUrStepName = StringField()
    lastUrPrevPerformerName = StringField()
    bpmn = DictField(null=True, required=False)
    bpmnName = StringField(null=True, required=False)
    bpmnForCreate = StringField(max_length=255, null=True, required=False)
    name = StringField(max_length=255, null=True, required=False)
    stepsWithDates = DictField(null=True, required=False)
    performer = ObjectIdField()
    chartPerformer = IntField()
    prevPerformer = DictField(null=True, required=False)

    steps = ListField(null=True, required=False)
    pastSteps = ListField(null=True, required=False)
    engineInstance = StringField(null=True, required=False)
    formData = DictField(null=True, required=False)
    postDate = DateTimeField(
        default=datetime.now,
        required=False,
        null=True
    )
    startProcessDate = DateTimeField(
        default=datetime.now,
        required=False,
        null=True
    )
    isHide = BooleanField(default=False)
    lunchedProcessId = ObjectIdField()
    allPerformers = ListField(required=False, default=[])


class ReportBpmnsPermissions(Document):
    chartId = IntField(default=0)
    companyId = IntField(default=0)
    bpmns = ListField(default=[])
    bpmnsDetail = ListField(default=[])


class ReportData(Document):
    chartId = IntField(default=0)
    lpId = ObjectIdField(null=True, required=False)
    lpName = StringField(null=True, required=False)
    bpmnId = ObjectIdField(null=True, required=False)
    bpmnName = StringField(null=True, required=False)
    companyId = IntField(default=0)
    lpStartDate = DateTimeField()
    lpEndDate = DateTimeField()
    lpPosition = ObjectIdField()
    lpPositionName = StringField()
    lpChart = IntField()
    lpChartName = StringField()
    isDone = BooleanField(default=False)

    formData = DictField(default={})
    processObjs = ListField(default=[])


class Statistic(Document):
    position_id = ObjectIdField()
    Lp = IntField(default=0)
    Lpa = IntField(default=0)
    Dpa = IntField(default=0)
    Mp = IntField(default=0)
    newLp = IntField(default=0)
    newMp = IntField(default=0)


"""
this module is for saving datatables selections
"""


class TableSelectedItems(Document):
    bpmn = ObjectIdField(required=True)  # reference to Bpmn
    process = ObjectIdField(required=False, null=True, )  # process
    completedProcess = ObjectIdField(required=False, null=True, )  # completedProcess
    taskID = StringField(required=False, null=True, max_length=100, )
    objID = StringField(required=False, null=True, max_length=100, )
    dataTableID = ReferenceField(DataTable, required=False, null=True)
    dataTableValueID = ReferenceField(DataTableValues, required=False, null=True)
    storeData = DictField()  # for dynamic fields
    postDate = DateTimeField(default=datetime.now, required=False, null=True)
    positionID = ObjectIdField()
    companyID = IntField(null=False, required=True)


class ExtraDataForTableSelectedItems(Document):
    postDate = DateTimeField(default=datetime.now, required=False, null=True)
    positionID = ObjectIdField()
    companyID = IntField(null=False, required=True)
    tableSelectedItemsLink = ReferenceField(TableSelectedItems, required=True, null=False)
    values = ListField()
    desc = DictField()  # for dynamic fields


"""
this module is for saving sqltables selections
"""


class SqlTableSelectedItems(Document):
    bpmn = ObjectIdField(required=True)  # reference to Bpmn
    process = ObjectIdField(required=False, null=True, )  # process
    completedProcess = ObjectIdField(required=False, null=True, )  # completedProcess
    taskID = StringField(required=False, null=True, max_length=100, ) # storing task name name task_sada
    taskName = StringField(required=False, null=True, max_length=100, ) # storing task name name task_sada
    objID = StringField(required=False, null=True, max_length=100, ) # storing task unique obj name
    sqlDataTableLinkerField = StringField(required=False, null=True, max_length=100, )
    sqlDataTableLinkerValue = StringField(required=False, null=True, max_length=100, )
    connectionID = ReferenceField(Connections, required=False, null=True)
    connectionPoolID = ReferenceField(ConnectionPools, required=False, null=True)
    storeData = DictField()  # for dynamic fields
    postDate = DateTimeField(default=datetime.now, required=False, null=True)
    positionID = ObjectIdField()
    companyID = IntField(null=False, required=True)


class ExtraSqlDataForTableSelectedItems(Document):
    postDate = DateTimeField(default=datetime.now, required=False, null=True)
    positionID = ObjectIdField()
    companyID = IntField(null=False, required=True)
    sqlTableSelectedItemsLink = ReferenceField(SqlTableSelectedItems, required=True, null=False)
    values = ListField()
    desc = DictField()  # for dynamic fields
