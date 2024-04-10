from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets

from amspApp.Infrustructures.Classes.DateConvertors import getCurrentYearShamsi, \
    getCurrentMonthShamsi, getCurrentDayShamsi


class PageLoaderApi(viewsets.ModelViewSet):

    def template_base(self, request):
        year = getCurrentYearShamsi()
        month = getCurrentMonthShamsi()

        return render_to_response(
            'Edari/ez/base.html',
            {'frm': {
                'year': year,
                'month': month
            }},
            context_instance=RequestContext(request))

    def template_base_ez_item(self, request):
        year = getCurrentYearShamsi()
        month = getCurrentMonthShamsi()

        return render_to_response(
            'Edari/ez/template_base_ez_item.html',
            {'frm': {
                'year': year,
                'month': month
            }},
            context_instance=RequestContext(request))

    def template_base_ez_list(self, request):
        year = getCurrentYearShamsi()
        month = getCurrentMonthShamsi()

        return render_to_response(
            'Edari/ez/template_base_ez_list.html',
            {'frm': {
                'year': year,
                'month': month
            }},
            context_instance=RequestContext(request))

    def template_base_ez_report(self, request):
        year = getCurrentYearShamsi()
        month = getCurrentMonthShamsi()
        day = getCurrentDayShamsi()
        return render_to_response(
            'Edari/ez/template_reports.html',
            {'frm': {
                'year': year,
                'month': month,
                'day': day
            }},
            context_instance=RequestContext(request))
