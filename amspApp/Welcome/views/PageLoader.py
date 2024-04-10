from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import views


class welcomeBase(views.APIView):
    def get(self, request):
        return render_to_response('others/base.html', {}, context_instance=RequestContext(request))
class welcomePage(views.APIView):
    def get(self, request):
        return render_to_response('others/welcomes/owner/1_welcomePage.html', {}, context_instance=RequestContext(request))
class welcomeSelectNames(views.APIView):
    def get(self, request):
        return render_to_response('others/welcomes/owner/2_setName.html', {}, context_instance=RequestContext(request))
class welcomeSelectPics(views.APIView):
    def get(self, request):
        return render_to_response('others/welcomes/owner/3_selectpics.html', {}, context_instance=RequestContext(request))
class welcomeCompleted(views.APIView):
    def get(self, request):
        return render_to_response('others/welcomes/owner/4_completed.html', {}, context_instance=RequestContext(request))
class welcomeCompleted(views.APIView):
    def get(self, request):
        return render_to_response('others/welcomes/owner/4_completed.html', {}, context_instance=RequestContext(request))
