from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from amspApp.CompaniesManagment.Positions.models import Position
from amspApp.Letter.models import Inbox
from amspApp.Letter.serializers.InboxSerializer import InboxSerializer
from amspApp.Letter.views.InboxListView import InboxListViewSet

__author__ = 'mohammad'



class InboxPreviewViewSet(viewsets.ModelViewSet):
    serializer_class = InboxListViewSet
    lookup_field = "id"

    def template_view_base(self, request, *args, **kwargs):
        return render_to_response(
            "letter/Preview/base.html",
            {},context_instance=RequestContext(request))

    def template_view(self, request, *args, **kwargs):
        return render_to_response(
            "letter/Preview/preview.html",
            {},context_instance=RequestContext(request))



