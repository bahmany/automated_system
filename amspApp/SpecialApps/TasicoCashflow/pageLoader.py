from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets


class PageLoaderApi(viewsets.ModelViewSet):
    def base(self, request):
        return render_to_response(
            'SpecialApps/****Cashflow/base.html',
            {},
            context_instance=RequestContext(request))