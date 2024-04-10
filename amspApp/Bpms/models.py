from datetime import datetime
from mongoengine import *


class LunchedProcess(Document):
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
    ==================
    positionName
        creators name
    """

    user_id = IntField()
    position_id = ObjectIdField()
    positionName = StringField()
    bpmn = DictField(null=True, required=False)
    bpmnForCreate = StringField(max_length=255, null=True, required=False)
    name = StringField(max_length=255, null=True, required=False)
    thisStep = StringField(max_length=255, null=True, required=False)
    thisPerformers = ListField(required=False, default=[])
    thisPerformerType = IntField()
    thisChartPerformer = IntField()
    previousPerformer = DictField(required=False, null=True, default={})
    pastSteps = ListField(required=False, default=[])
    engineInstance = StringField(null=True, required=False)
    formData = DictField(null=True, required=False)
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

    """

    user_id = IntField()
    positionName = StringField()
    position_id = ObjectIdField()
    bpmn = DictField(null=True, required=False)
    bpmnForCreate = StringField(max_length=255, null=True, required=False)
    name = StringField(max_length=255, null=True, required=False)
    thisStep = StringField(max_length=255, null=True, required=False)
    thisPerformers = ListField(required=False, default=[])
    thisPerformerType = IntField()
    thisChartPerformer = IntField()
    previousPerformer = DictField(required=False, null=True, default={})
    pastSteps = ListField(required=False, default=[])
    engineInstance = StringField(null=True, required=False)
    formData = DictField(null=True, required=False)
    hasApprove = BooleanField(default=True)
    hasApproveMainId = ObjectIdField(null=True, required=False)
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
        A dict that contains steps(which you have approve them) with their comeToInbox and done date, like this:
        {'STEP NAME':{'comeToInbox':"THE DATE", 'done':"THE DATE"},
         'STEP NAME':{'comeToInbox':"THE DATE", 'done':"THE DATE"},
             ...
        }

    ===============
    bpmn
        bpmn object

    ===============
    steps
        A list that contains steps(which you have approve them)

    ===============
    performer_id
        PositionId of performer who have approve these steps

    ===============================
    chartPerformer
        ChartId of performer who have approve these steps

    ===============================
    pastSteps
        ReferenceField to LunchedProcess.pastSteps

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
        {'id':'POSITION ID','name':'PROFILE NAME'}

    ===============================
    nextPerformer
        The next performer :
        {'id':'POSITION ID','name':'PROFILE NAME'}

    """

    user_id = IntField()
    position_id = ObjectIdField()
    positionName = StringField()
    lunchedProcessId = ObjectIdField()
    bpmn = DictField(null=True, required=False)
    name = StringField(max_length=255, null=True, required=False)
    stepsWithDates = DictField(null=True, required=False, default={})
    performer = ObjectIdField()
    chartPerformer = IntField()
    steps = ListField(null=True, required=False, default=[])
    pastSteps = ReferenceField(LunchedProcess, required=False)
    engineInstance = StringField(null=True, required=False)
    formData = DictField(null=True, required=False)
    startProcessDate = DateTimeField(
        default=datetime.now,
        required=False,
        null=True
    )


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

    """

    user_id = IntField()
    position_id = ObjectIdField()
    positionName = StringField()
    bpmn = DictField(null=True, required=False)
    bpmnForCreate = StringField(max_length=255, null=True, required=False)
    name = StringField(max_length=255, null=True, required=False)
    stepsWithDates = DictField(null=True, required=False)
    performer = ObjectIdField()
    chartPerformer = IntField()
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


class Statistic(Document):
    position_id = ObjectIdField()
    Lp = IntField(default=0)
    Lpa = IntField(default=0)
    Dpa = IntField(default=0)
    Mp = IntField(default=0)
    newLp = IntField(default=0)
    newMp = IntField(default=0)


class ProcessFormAdvanceTable(Document):
    position_id = ObjectIdField()
    # bpmsID = ObjectIdField()
    # processID = ObjectIdField()
    # fieldID = StringField()
    table = DictField()

