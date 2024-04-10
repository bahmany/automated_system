from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets, permissions, views
from rest_framework.response import Response

from amspApp.Administrator.permission.IsSuperUser import IsSuper


class IndexApiViewSet(views.APIView):
    permission_classes = (IsSuper,)
    def get(self, request):
        return render_to_response(
            'Administrator/Dashboard/index.html',
            {},
            context_instance=RequestContext(request))


class DashboardBaseApiViewSet(views.APIView):
    permission_classes = (IsSuper,)
    def get(self, request):




        return render_to_response(
            'Administrator/Dashboard/base.html',
            {},
            context_instance=RequestContext(request))
