from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets

from amspApp.Infrustructures.Classes.DateConvertors import getCurrentYearShamsi, \
    getCurrentMonthShamsi


class PageLoaderApi(viewsets.ModelViewSet):

    def template_base(self, request):
        year = getCurrentYearShamsi()
        month = getCurrentMonthShamsi()

        return render_to_response(
            'Edari/hz/base.html',
            {'frm': {

                'year': year,
                'month': month

            }
            },
            context_instance=RequestContext(request))
