from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import views


class ControlProjectBaseTemplateView(views.APIView):
    def get(self, request, *args, **kwargs):
        return render_to_response(
            "ControlProject/base.html",
            {}, context_instance=RequestContext(request))