import pytz
from amspApp.Notifications.models import HasNotifications

from amspApp.Notifications.serializers.NotificationSerializer import HasNotificationsSerializer


class SessionTranslator(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            return
            notiInstance = HasNotifications.objects.filter(userID=request.user.id)
            if notiInstance.count() == 0:
                newData = {
                    "sessionID": request.COOKIES['sessionid'],
                    "userID": request.user.id
                }
                ss = HasNotificationsSerializer(data=newData)
                ss.is_valid(raise_exception=True)
                ss.create(validated_data=ss.validated_data)
            else:
                newData = {
                    "sessionID": request.COOKIES['sessionid']
                }
                ss = HasNotificationsSerializer(instance=notiInstance[0], data=newData)
                ss.is_valid(raise_exception=True)
                ss.update(notiInstance[0],ss.validated_data)





