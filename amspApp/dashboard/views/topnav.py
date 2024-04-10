from datetime import datetime

import pytz
from django.views.generic import TemplateView
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
import time

from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh


class TopNavView(TemplateView):
    template_name = 'broadcast_chat.html'

    def get(self, request, *args, **kwargs):
        return

        profile = self.handleCurrentUser(request)
        userAvatar = profile.extra['profileAvatar']['url'].split("=")[0] + "=thmum100_" + \
                     profile.extra['profileAvatar']['url'].split("=")[1] if profile.extra['profileAvatar'][
                                                                                'url'] != '/static/images/avatar_empty.jpg' else '/static/images/avatar_empty.jpg'
        # request.data['entryDate']=convertTimeZoneToUTC(request.user.timezone, request.data['entryDate'])
        # settingstime_zone = pytz.timezone(request.user.timezone)
        # enrtyDate = settingstime_zone.localize(datetime.strptime(datetime.now(), "%Y-%m-%dT%H:%M")).astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M')
        cc = datetime.now(pytz.timezone(request.user.timezone))
        # hh = lambda: int(round(time.time() * 1000))
        data = {
            'currentUser': request.user.username,
            'userAvatar': userAvatar,
            'currenttime': int((time.mktime(cc.timetuple()) + cc.microsecond / 1000000.0) * 1000),
            # (cc.day * 24 * 60 * 60 + cc.second) * 1000 + cc.microsecond / 1000.0 #int(3600000 * cc.hour + 60000 * cc.minute + 1000 * cc.second)
            'currentdatesh': mil_to_sh(datetime.now()),
            'currentdatemil': datetime.now().strftime("%Y/%m/%d")
            # 'currenttime':int((time.mktime(datetime.now().timetuple()) + datetime.now().microsecond/1000000.0)*1000)
            # 'currenttime':time.time()*1000

        }



        welcome = RedisMessage('Hello everybody')  # create a welcome message to be sent to everybody
        RedisPublisher(facility='foobar', broadcast=True).publish_message(welcome)


        return super(TopNavView, self).get(request, *args, **kwargs)