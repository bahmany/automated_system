import pytz

from django.utils import timezone

class ProxyMiddleware(object):

    def process_response(self, request, response):

        return response
