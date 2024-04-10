from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework_mongoengine import viewsets


class MorekhasiRoozanehiViewSet(viewsets.ModelViewSet):

    def template_base(self, request):
        return render_to_response(
            'Edari/Morekhasi/Roozaneh/base.html',
            {},
            context_instance=RequestContext(request))
