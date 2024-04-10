from datetime import datetime

from mongoengine import Document, DateTimeField, IntField, DictField, ListField, StringField, ReferenceField
from rest_framework_mongoengine.fields import ObjectIdField

from amspApp.BI.DataTables.models import DataTable


class BIDashboardPage(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    positionID = IntField()
    previous_page = ListField()  # برای مدیریت رویژن های مختلف
    groups_allowed = ListField()  # برای مدیریت دسترسی ها
    users_allowed = ListField()  # برای مدیریت دسترسی ها
    pageTitle = StringField(required=True, unique=True)
    details = DictField()  # برای ذخیره سازی تمامی مشخصات قرارگیری چارت


class BIGroups(Document):
    groupTitle = StringField(required=True, unique=True)
    groupMember = ListField()
    positionID = IntField()


class BIChart(Document):
    chartTitle = StringField(required=True, unique=True)
    details = DictField()
    positionID = IntField()


class BIDatasource(Document):
    datasourceTitle = StringField(required=True, unique=True)
    details = DictField()
    positionID = IntField()
    airflow_connection_id = StringField(required=True, unique=True)
    dateOfPost = DateTimeField(default=datetime.now())


class BISqls(Document):
    sqlTitle = StringField(required=True, unique=True)
    positionID = IntField()
    dateOfPost = DateTimeField(default=datetime.now())
    lastRevision = ListField()
    """
    type_of_datasource : by 
    1 = airflow
    2 = rahsoon datatabales
    3 = rahsoon statics
    4 = rahsoon specific reports like :
            آمار خروج ها - آمار حواله فورش ها و ...
    
    """
    type_of_datasource = IntField()
    slqscript_feeder = StringField(required=False, null=True)  # when type_of_datasource = 1
    slqscript_selector = StringField(required=False, null=True)  # when type_of_datasource = 1
    datatable_id = ReferenceField(DataTable, required=False, null=True)  # when type_of_datasource = 2
    statics_id = ObjectIdField(required=False, )  # when type_of_datasource = 3
    def_name = StringField(required=False, null=True)  # when type_of_datasource = 4
    sql_runner_schedual = IntField(required=False, null=True)

"""
structures
برای گزارهای فروش :
کد مشتری
نام مشتری
کد محصول
میزان
مبلغ

"""



class BIStorage(Document):
    BISqlsLink = ReferenceField(BISqls, required=True)
    data = DictField()
    dateOfPost = DateTimeField(default=datetime.now())
    

class BIBanksFromSpreadSheet(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    data = ListField()


class BIMenu(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    title = StringField(unique=True)
    groups_allowed = ListField()  # برای مدیریت دسترسی ها
    users_allowed = ListField()  # برای مدیریت دسترسی ها

class BIMenuItem(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    order = IntField(null=True)
    title = StringField()
    menu = ReferenceField(BIMenu, null=False)
    parent = ReferenceField("self", null=True, required=False)
    page = ReferenceField(BIDashboardPage, null=False)


