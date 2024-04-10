from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets


class DMSViewSet(viewsets.ModelViewSet):

    def dmsBase(self, request, *args, **kwargs):
        return render_to_response('DMS/baseIframe.html', {},
                                  context_instance=RequestContext(request))