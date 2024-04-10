from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets

from amspApp.Infrustructures.Classes.DateConvertors import getCurrentYearShamsi, \
    getCurrentMonthShamsi, getCurrentDayShamsi


class PageLoaderApi(viewsets.ModelViewSet):

    def template_base(self, request):
        return render_to_response(
            'Edari/base.html',
            {},
            context_instance=RequestContext(request))


    def template_edariReportBase(self, request):
        return render_to_response(
            'Edari/reports/base.html',
            {},
            context_instance=RequestContext(request))


    def template_edariReportTaradodMahaneh(self, request):
        return render_to_response(
            'Edari/reports/my_taradod.html',
            {},
            context_instance=RequestContext(request))


    def template_edariReportMandehMorekhasi(self, request):
        return render_to_response(
            'Edari/reports/mandeh_morekhasi.html',
            {},
            context_instance=RequestContext(request))


    def template_edariReportMorekhsiSaati(self, request):
        return render_to_response(
            'Edari/reports/morekhasi_saati.html',
            {},
            context_instance=RequestContext(request))


    def template_edariReportMorekhsiRoozaneh(self, request):
        return render_to_response(
            'Edari/reports/morekhasi_roozaneh_list.html',
            {},
            context_instance=RequestContext(request))


    def template_edariEmzaKonandeha(self, request):
        if request.user.groups.filter(name="edari_manager").count() == 0:
            return render_to_response('Financial/cog/noaccess.html', {}, context_instance=RequestContext(request))
        return render_to_response(
            'Edari/EmzaKonandeha/base.html',
            {},
            context_instance=RequestContext(request))
