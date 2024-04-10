from datetime import datetime
from mongoengine import *


class Shakhes(Document):
    user_id = IntField()
    position_id = ObjectIdField()
    position_name = StringField(max_length=255, required=False)
    bpmn_id = ObjectIdField(required=True)
    is_all_steps = BooleanField(default=True)
    step_id = StringField(max_length=255, required=False)
    bpmn_name = StringField(max_length=255, required=False)
    step_name = StringField(max_length=255, required=False)
    time_period= IntField(required=True)
    # baraye ziriye true is running process
    done_or_run = BooleanField(default=True)
    # 1== tedad
    # 2== zaman
    # va ...
    messurment = IntField(default=1)
    min_mess = IntField(required=True)
    start_warn = IntField(required=True)
    start_danger = IntField(required=True)
    max_mess = IntField(default=1)
    company_id = IntField(default=1)
    name = StringField(max_length=50, required=True)
    extra = DictField(null=True, required=False, default={})
    postDate = DateTimeField(null=True, required=False, default=datetime.now())

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.postDate = datetime.now()
        return super(Shakhes, self).save(*args, **kwargs)