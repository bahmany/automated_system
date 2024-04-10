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



class InboxForwardViewSet(viewsets.ModelViewSet):
    serializer_class = InboxListViewSet
    lookup_field = "id"



    def template_view(self, request, *args, **kwargs):
        return render_to_response(
            "letter/Forward/RecieversModal.html",
            {},context_instance=RequestContext(request))



    @detail_route(methods=["post"])
    def send(self,request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        inboxInstance = Inbox.objects.get(
            id=kwargs["id"],
            currentPositionID=pos.id)
        InboxSerializer().Forward(pos, request.data, inboxInstance)
        return Response({})

