from mongoengine import *

from datetime import datetime

"""
this model is the main one which store main puspose of a company in sprecific time
"""


class CalYears(Document):
    postDate = DateTimeField(default=datetime.now())
    startDate = DateTimeField(required=True)
    endDate = DateTimeField(required=True)
    positionID = IntField(required=True)
    companyID = IntField(required=True)
    title = StringField(required=True)
    desc = StringField()
    exp = DictField()

    def clean(self):
        startDate = self._data.get("startDate")
        endDate = self._data.get("endDate")
        errors = {}
        if endDate < startDate:
            errors['endDate'] = ValidationError("تاریخ پایان می بایست بیشتر از تاریخ شروع باشد", field_name='endDate')
        if errors:
            raise ValidationError('ValidationError', errors=errors)


"""
this model save users access to year
"""


class CalYearsShare(Document):
    postDate = DateTimeField(default=datetime.now())
    postPositionID = IntField(required=True)
    calYearID = ReferenceField(CalYears)
    positionID = IntField(required=True)
    """
    perType :
      0 = readonly
      1 = editable
      2 = access denied
    """
    perType = IntField(default=0)


class OutcomeTypes(Document):
    positionID = IntField()
    postDate = DateTimeField(default=datetime.now())
    companyID = IntField()
    name = StringField()
    countType = IntField()


class IncomeTypes(Document):
    positionID = IntField()
    postDate = DateTimeField(default=datetime.now())
    companyID = IntField()
    name = StringField()
    countType = IntField()


"""
in this project we have some main projects
these projects have some benefit and costs
these project can be related to other project
it could be complement of other one
or this project need to be run after another project completed
these project must have some other projects
"""


class CalProjects(Document):
    positionID = IntField()
    postDate = DateTimeField(default=datetime.now())
    """Years which project is belong to"""
    calYearID = ReferenceField(CalYears)
    companyID = IntField()
    name = StringField()
    isItContinuesToEnd = BooleanField()
    startDate = DateTimeField()  #
    endDate = DateTimeField(required=False)  # if isItContinuesToEnd = True then this field is nothing


class CalSubProjects(Document):
    positionID = IntField()
    postDate = DateTimeField(default=datetime.now())
    """Years which project is belong to"""
    calProjects = ReferenceField(CalProjects)
    name = StringField()
    isItContinuesToEnd = BooleanField()
    startDate = DateTimeField()  #
    endDate = DateTimeField(required=False)  # if isItContinuesToEnd = True then this field is nothing
    """
    relatedProjects = [{
        projectID,
        rpType : 1= using from this project benefits 2= charge benefit from this project to other
        amountPayment : rial
        amountTotal : Km
        donePercent = %
    }]
    """
    relatedProjects = ListField()
    parentSubProject = ObjectIdField(null=True, required=False)


class CalSubProjectsItems(Document):
    positionID = IntField()
    postDate = DateTimeField(default=datetime.now())
    canEditByOther = BooleanField(default=False)
    calSubProject = ReferenceField(CalSubProjects)
    startDate = DateTimeField()
    endDate = DateTimeField(required=False)
    cpiType = IntField()  # 1= Income    2= Outcome 3= Both
    calOutcomeTypes = ReferenceField(OutcomeTypes)
    calIncomeTypes = ReferenceField(IncomeTypes)
    calOutcomeValue = FloatField()
    calIncomeValue = FloatField()


class WBSResource(Document):
    name = StringField()


class WBSResourceItems(Document):
    name = StringField()
    resourceLink = ReferenceField(WBSResource)


"""
Parameter	Description
ID:	(required) a unique numeric ID used to identify each row
Name:	(required) the task Label
Start:	(required) the task start date, can enter empty date ('') for groups. You can also enter specific time (e.g. 2013-02-20 09:00) for additional precision or half days
End:	(required) the task end date, can enter empty date ('') for groups
Class:	(required) the css class for this task
Link:	(optional) any http link to be displayed in tool tip as the "More information" link.
Mile:	(optional) indicates whether this is a milestone task - Numeric; 1 = milestone, 0 = not milestone
Res:	(optional) resource name
Comp:	(required) completion percent, numeric
Group:	(optional) indicates whether this is a group task (parent) - Numeric; 0 = normal task, 1 = standard group task, 2 = combined group task*
Parent:	(required) identifies a parent pID, this causes this task to be a child of identified task. Numeric, top level tasks should have pParent set to 0
Open:	(required) indicates whether a standard group task is open when chart is first drawn. Value must be set for all items but is only used by standard group tasks. Numeric, 1 = open, 0 = closed
Depend:	(optional) comma separated list of id's this task is dependent on. A line will be drawn from each listed task to this item. Each id can optionally be followed by a dependency type suffix. Valid values are: 'FS' - Finish to Start (default if suffix is omitted), 'SF' - Start to Finish, 'SS' - Start to Start, 'FF' - Finish to Finish. If present the suffix must be added directly to the id e.g. '123SS'
Caption:	(optional) caption that will be added after task bar if CaptionType set to "Caption"
Notes:	(optional) Detailed task information that will be displayed in tool tip for this task
Gantt:	(required) javascript JSGantt.GanttChart object from which to take settings. Defaults to "g" for backwards compatibility
"""


class WBS(Document):
    id_num = IntField()  # numberic id for parent
    name = StringField()
    start = DateTimeField(required=False, null=True)
    end = DateTimeField(required=False, null=True)
    css_class = StringField()
    http_link = StringField()
    mile = IntField()
    res = ReferenceField(WBSResource)
    comp = IntField()
    group = IntField()
    parent = IntField()
    open = IntField()
    depend = ListField()
    caption = StringField()
    notes = StringField()
