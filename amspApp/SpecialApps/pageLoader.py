from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets


class PageLoaderApi(viewsets.ModelViewSet):
    def index(self, request):
        return render_to_response(
            'SpecialApps/index.html',
            {},
            context_instance=RequestContext(request))


    def base(self, request):
        return render_to_response(
            'SpecialApps/base.html',
            {},
            context_instance=RequestContext(request))
    def home(self, request):
        return render_to_response(
            'SpecialApps/home.html',
            {},
            context_instance=RequestContext(request))


    def dash(self, request):
        return render_to_response('SpecialApps/others/dash.html', {}, context_instance=RequestContext(request))