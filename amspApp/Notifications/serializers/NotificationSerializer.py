from asq.initiators import query
from datetime import datetime

from django.contrib.auth.models import Group
from django.core.cache import cache
from amspApp.Notifications.models import Notifications, HasNotifications, GoogleToken, SimpleNotificatoin
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer
from fcm_django.models import FCMDevice

from amspApp.amspUser.models import MyUser
from amspApp.tasks import sendNotification
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage


class NotificationsSerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = Notifications

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    def changesHappened(self, userID_int, userSessionStr=None):
        cache.set(str(userID_int) + "TopNotification", None)
        # cache.set(str(userID_int)+"hasNotification", True)
        notiInstance = HasNotifications.objects.filter(userID=userID_int)
        if notiInstance.count() == 0:
            newData = {
                "userID": userID_int,
                "dateOfPost": datetime.now(),
                "has": True}
            ss = HasNotificationsSerializer(data=newData)
            ss.is_valid(raise_exception=True)
            ss.create(validated_data=ss.validated_data)
        else:
            ss = HasNotificationsSerializer(
                instance=notiInstance[0],
                data={
                    "has": True,
                    "dateOfPost": datetime.now()
                },
                partial=True)
            ss.is_valid(raise_exception=True)
            ss.update(instance=notiInstance[0], validated_data=ss.validated_data)

    def markNotificationRead(self, userID_int):
        cache.set(str(userID_int) + "TopNotification", None)
        # cache.set(str(userID_int)+"hasNotification", True)
        notiInstance = HasNotifications.objects.filter(userID=userID_int)
        if notiInstance.count() == 0:
            newData = {
                "userID": userID_int,
                "dateOfPost": datetime.now(),
                "has": True}
            ss = HasNotificationsSerializer(data=newData)
            ss.is_valid(raise_exception=True)
            ss.create(validated_data=ss.validated_data)
        else:
            ss = HasNotificationsSerializer(
                instance=notiInstance[0],
                data={
                    "has": False},
                partial=True)
            ss.is_valid(raise_exception=True)
            ss.update(instance=notiInstance[0], validated_data=ss.validated_data)

    def create(self, validated_data):
        result = super(NotificationsSerializer, self).create(validated_data)
        self.changesHappened(result.userID)
        getDistinctTypes = Notifications.objects.filter(userID=result.userID).distinct(field='type')
        fin = []
        for itm in getDistinctTypes:
            objs = NotificationsSerializer(
                instance=Notifications.objects.filter(userID=result.userID, type=itm).order_by('-dateOfPost').limit(10),
                many=True).data
            objs = [dict(i) for i in objs]
            fin += objs
        fin = list(query(fin).order_by_descending(lambda x: x['dateOfPost']))
        cache.set(str(result.userID) + "TopNotification", fin)
        return result

    def save(self, **kwargs):
        result = super(NotificationsSerializer, self).save(**kwargs)
        userID = self.data.get("userID")
        notif = NotificationsSerializer(instance=result).data
        sendNotification.delay(userID, notif, )
        username = MyUser.objects.get(id=userID)
        redis_publisher = RedisPublisher(facility='foobar', users=[username.username])
        message = RedisMessage(str(notif['type']) + "___" + str(notif['id']))
        redis_publisher.publish_message(message, expire=60)
        # sendNotification(userID, notif, )
        return result

    def send_to_group_message_with_ws(self, msg_type, msg_content, group_name, msg_body):
        msg = str(msg_type) + "___" + msg_content
        users = list(Group.objects.get(name=group_name).user_set.all())

        for u in users:
            redis_publisher = RedisPublisher(facility='foobar', users=[u.username])
            dt = {
                'type': msg_type,
                'typeOfAlarm': 1,
                'priority': 1,
                'informType': 1,
                'userID': u.id,
                'dateOfPost': datetime.now(),
                'extra': {
                    'msg_type': msg_type,
                    'msg_content': msg_content,
                    'group_name': group_name,
                    'msg_body': msg_body,
                }
            }
            ser = NotificationsSerializer(data=dt)
            ser.is_valid(raise_exception=True)
            ser = ser.save()
            message = RedisMessage(msg + "___" + str(ser.id))
            redis_publisher.publish_message(message, expire=60)


class GoogleTokenSerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = GoogleToken

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class HasNotificationsSerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = HasNotifications

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    def create(self, validated_data):
        validated_data["dateOfPost"] = datetime.now()
        return super(HasNotificationsSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        return super(HasNotificationsSerializer, self).update(instance, validated_data)


class SimpleNotificatoinSerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = SimpleNotificatoin

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)
