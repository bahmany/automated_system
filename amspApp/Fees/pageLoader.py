from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets

from amspApp.Infrustructures.Classes.DateConvertors import getCurrentYearShamsi, \
    getCurrentMonthShamsi, getCurrentDayShamsi


class PageLoaderApi(viewsets.ModelViewSet):

    def template_base(self, request):
        return render_to_response(
            'Fees/base.html',
            context_instance=RequestContext(request))
