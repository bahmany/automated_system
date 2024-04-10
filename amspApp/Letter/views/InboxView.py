from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework_mongoengine import viewsets

from amspApp.Letter.serializers.InboxSerializer import InboxSerializer
from amspApp._Share.ListPagination import ListPagination


class InboxViewSet(viewsets.ModelViewSet):

    pagination_class = ListPagination
    lookup_field = "id"
    serializer_class = InboxSerializer



    def template_view_base(self, request, *args, **kwargs):
        return render_to_response(
            # "letter/InboxBase.html",
            "letter/base.html",
            {},context_instance=RequestContext(request))

    def template_view_inboxParts(self, request, *args, **kwargs):
        return render_to_response(
            # "letter/InboxBase.html",
            "letter/Inbox/inboxParts.html",
            {},context_instance=RequestContext(request))







