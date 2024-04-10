from datetime import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets

from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh, mil_to_sh_with_time


class PageLoaderApi(viewsets.ModelViewSet):

    def template_view_read(self, request):
        return render_to_response(
            'Material/base.html',
            {},
            context_instance=RequestContext(request))

    def template_locations(self, request):
        return render_to_response(
            'Material/locations.html',
            {},
            context_instance=RequestContext(request))

    def template_materialbaskol(self, request):
        return render_to_response(
            'Material/baskol.html',
            {},
            context_instance=RequestContext(request))

    def template_report_base(self, request):
        return render_to_response(
            'Material/reports/base.html',
            {},
            context_instance=RequestContext(request))

    def template_materialfromBaskolToAnbar(self, request):
        return render_to_response(
            'Material/voroodkhorooj/baskol_to_anbar.html',
            {},
            context_instance=RequestContext(request))

    def template_materialBasket(self, request):
        serverdate = mil_to_sh_with_time(datetime.now())

        return render_to_response(
            'Material/barname/basket.html',
            {'serverdate': serverdate},
            context_instance=RequestContext(request))

    def template_materialBarnameBase(self, request):
        return render_to_response(
            'Material/barname/base.html',
            {},
            context_instance=RequestContext(request))

    def template_report_1(self, request):
        return render_to_response(
            'Material/reports/report_1.html',
            {},
            context_instance=RequestContext(request))

    def template_report_2(self, request):
        return render_to_response(
            'Material/reports/report_2.html',
            {},
            context_instance=RequestContext(request))

    def template_materialBarnameTolid(self, request):
        return render_to_response(
            'Material/tolid_mavad_az_barnamerizi/base.html',
            {},
            context_instance=RequestContext(request))

    def template_popupBaskol(self, request):
        return render_to_response(
            'Material/baskolpopup.html',
            {},
            context_instance=RequestContext(request))

    def template_materialVoroodKhrooj(self, request):
        return render_to_response(
            'Material/voroodkhorooj/base.html',
            {},
            context_instance=RequestContext(request))

    def template_tolidSaleConvSale(self, request):
        return render_to_response(
            'Material/tolid_sale/tolidSaleConvSale.html',
            {},
            context_instance=RequestContext(request))

    def template_tolidSaleConvSaleItem(self, request):
        return render_to_response(
            'Material/tolid_sale/tolidSaleConvSaleItem.html',
            {},
            context_instance=RequestContext(request))

    def template_materialBarcodeList(self, request):
        return render_to_response(
            'Material/voroodkhorooj/barcode_list.html',
            {},
            context_instance=RequestContext(request))

    def template_popupMasraf(self, request):
        return render_to_response(
            'Material/voroodkhorooj/masrafpopup.html',
            {},
            context_instance=RequestContext(request))

    def template_fromQCBlackplate(self, request):
        return render_to_response(
            'Material/voroodkhorooj/fromQCBlackplate.html',
            {},
            context_instance=RequestContext(request))

    def template_tolidSaleConv(self, request):
        return render_to_response(
            'Material/tolid_sale/base.html',
            {},
            context_instance=RequestContext(request))
