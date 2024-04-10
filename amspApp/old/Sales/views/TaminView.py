from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework_mongoengine import viewsets


class TaminViewSet(viewsets.ModelViewSet):

    def template_view_base(self, request):
        return render_to_response('Sales/Tamin/base.html', {}, context_instance=RequestContext(request))

    def template_view_SalesTaminProjects(self, request):
        return render_to_response('Sales/Tamin/TaminProjects/base.html', {}, context_instance=RequestContext(request))

    def template_view_tamin_Details(self, request):
        return render_to_response('Sales/Tamin/Details/base.html', {}, context_instance=RequestContext(request))

    def template_view_AdminTaminDakheli(self, request):
        return render_to_response('Sales/Tamin/TaminDakheli/Registered/base.html', {},
                                  context_instance=RequestContext(request))

    def template_view_AdminTaminDakheliDetails(self, request):
        return render_to_response('Sales/Tamin/TaminDakheli/Registered/details.html', {
            "frmNumbs": map(str, list(range(1, 27))), },
                                  context_instance=RequestContext(request))
