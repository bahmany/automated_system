import datetime

from django.core.cache import cache


class ActiveUserMiddleware:

    def process_request(self, request):
        current_user = request.user
        if request.user.is_authenticated():
            now = datetime.datetime.now()
            cache.set('%s_idle' % (current_user.id), now, 60 * 2 )
            cache.set('%s_active' % (current_user.id), now, 60 * 5 )
            cache.set('%s_lazy' % (current_user.id), now, 60 * 10)