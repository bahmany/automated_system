from datetime import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.CompaniesManagment.Secretariat.serializers.SecretariatsSerializers import SecretariatSerializer, \
    SecretariatSerializerPermission
from amspApp.CompaniesManagment.Secretariat.viewes.SecretariatsViews import SecretariatsViewSet
from amspApp.Infrustructures.Classes.PublicFilters import QuerySetFilter
from amspApp.Letter.models import CompanyRecieverGroup, CompanyReciever, Inbox, Letter, Recieved
from amspApp.Letter.search.InboxSearch import InboxSearchViewClass
from amspApp.Letter.serializers.LetterSecretariatSerializer import RecievedSerializer
from amspApp.Letter.serializers.LetterSerializer import LetterSerializer
from amspApp.Letter.views.InboxListView import InboxListViewSet
from amspApp.Letter.views.Secretariate.CompanyRecieverView import CompanyRecieverViewSet
from amspApp._Share.ListPagination import DetailsPagination


class RecievedViewSet(viewsets.ModelViewSet):
    pagination_class = DetailsPagination
    lookup_field = "id"
    serializer_class = RecievedSerializer
    queryset = Recieved.objects.all()


    def get_queryset(self):
        self.queryset = self.queryset.filter(inboxID=self.request.query_params['id']).order_by("-id")
        return self.queryset


    def update(self, request, *args, **kwargs):
        self.get_queryset()
        return super(RecievedViewSet, self).update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=request.user,
            company=request.user.current_company)
        request.data["positionID"] = pos.id
        # inboxInstace = Inbox.objects.get(id = request.data["inbox"])
        # request.data["inbox"] = inboxInstace.id
        return super(RecievedViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.get_queryset()
        return super(RecievedViewSet, self).destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.get_queryset()
        return super(RecievedViewSet, self).list(request, *args, **kwargs)



