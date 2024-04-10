from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework_mongoengine import viewsets



class TraceFromToViewSet(viewsets.ModelViewSet):



    def template_view(self, request):
        return render_to_response('Trace/base.html', {}, context_instance=RequestContext(request))
