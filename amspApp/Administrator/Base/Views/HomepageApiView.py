from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets, permissions, views
from rest_framework.response import Response

from amspApp.Administrator.permission.IsSuperUser import IsSuper


class HomepageApiViewSet(views.APIView):
    permission_classes = (IsSuper,)
    def get(self, request):
        return render_to_response(
            'Administrator/Dashboard/home.html',
            {},
            context_instance=RequestContext(request))
