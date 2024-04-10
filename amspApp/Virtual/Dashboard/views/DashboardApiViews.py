from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets, permissions, views
from rest_framework.response import Response


class DashboardBaseApiViewSet(views.APIView):

    def get(self, request):
        return render_to_response(
            'Virtual/Registration/base.html',
            {},
            context_instance=RequestContext(request))
