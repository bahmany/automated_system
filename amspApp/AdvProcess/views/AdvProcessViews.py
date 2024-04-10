import http.client
import re

from asq.initiators import query
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_mongoengine import viewsets

from amspApp.News.models import News
from amspApp.News.serializers.NewsSerializer import NewsSerializer
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class AdvProcessViewSetTempl(viewsets.ModelViewSet):

    def template_view(self, request):
        return render_to_response('AdvProcess/base.html', {}, context_instance=RequestContext(request))

class AdvProcessViewSet(APIView):


    def post(self, request):
        pass
    def get(self, request):
        conn = http.client.HTTPConnection(host="localhost", port=8080)
        pathAfterGen = request._request.path
        # if len(pathAfterGen) == 1:
        #     pathAfterGen = request._request.path.split("activiti-app")
        # pathAfterGen = pathAfterGen[1]


        regex = re.compile('^HTTP_')
        _header = dict((regex.sub('', header), value) for (header, value)
             in request.META.items() if header.startswith('HTTP_'))
        _header["HOST"]="localhost:8080"
        conn.request(method="GET", url= "/"+pathAfterGen, headers=_header)
        res = conn.getresponse()
        result = Response(res)
        result.data.headers = res.headers
        return result

        # with urllib.request.urlopen('http://python.org/') as response:

    def patch(self, request):
        pass
    def delete(self, request):
        pass



