import re

from django.shortcuts import render_to_response
from django.template import RequestContext
from mongoengine import Q
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Positions.models import Position
from amspApp.Contacts.models import *
from amspApp.Contacts.serializers.ContactsSerializer import ContactsSerializer, ContactsGroupsSerializer, \
    ContactsGroupItemsSerializer
from amspApp._Share.ListPagination import DetailsPagination

__author__ = 'mohammad'


class ContactsViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    # queryset = Profile.objects.all()
    serializer_class = ContactsSerializer
    pagination_class = DetailsPagination

    # queryset = Contacts.objects.all().order_by("-dateOfPost")

    def get_queryset(self):
        self.pagination_class.page_size = 20
        userID = self.request.user.id
        currentCompanyID = self.request.user.current_company.id
        otherCompanyIDsList = [x["company_id"] for x in
                                 list(Position.objects.filter(user_id=userID).exclude(
                                     company_id=currentCompanyID).values("company_id"))]
        queryset = Contacts.objects.filter(
            Q(userID=userID) |
            Q(extra__creatorCompanyID=currentCompanyID,
              publish__privacy=2,
              publish__this_companies_can_see=True) |
            Q(extra__creatorCompanyID__in=otherCompanyIDsList,
              publish__privacy=2,
              publish__this_companies_can_see=False,
              publish__other_companies_can_see=True)) \
            .order_by("-dateOfPost")
        if 'starred' in self.request.query_params:
            if bool(int(self.request.query_params['starred'])):
                queryset = queryset.filter(Q(extra__stars__starred=True, extra__stars__userID=userID))
        if 'group_id' in self.request.query_params:
            # getting group instact
            if self.request.query_params["group_id"]:
                if self.request.query_params["group_id"] != 'undefined':
                    groupInstace = ContactsGroups.objects.get(
                        id=self.request.query_params["group_id"],
                        userID=userID)
                    groupItems = ContactsGroupItems.objects.filter(
                        group=groupInstace
                    )
                    queryset = queryset.filter(Q(id__in=[str(x.member.id) for x in groupItems]))

        if 'q' in self.request.query_params:
            if self.request.query_params["q"]:
                if self.request.query_params["q"] != 'undefined':
                    regx = re.compile(self.request.query_params["q"], re.IGNORECASE)
                    # queryset = queryset.filter(Q(fields__fieldValue__contains = self.request.query_params["q"]))
                    queryset = queryset.filter(Q(fields__fieldValue=regx))

        # if 'f' in self.request.query_params:
        #     if self.request.query_params["f"]:
        #         if self.request.query_params["f"] != 'undefined':
        #             queryset = queryset.skip(int(self.request.query_params["f"]))
        # if 't' in self.request.query_params:
        #     if self.request.query_params["t"]:
        #         if self.request.query_params["t"] != 'undefined':
        #             queryset = queryset.limit(int(self.request.query_params["t"]))

        # if 'q' in self.request.query_params:

        # self.queryset = queryset

        # self.queryset.skip()
        self.queryset = queryset
        return queryset

    def list(self, request, *args, **kwargs):
        userID = request.user.id
        self.get_queryset()
        result = super(ContactsViewSet, self).list(request, *args, **kwargs)

        for r in result.data['results']:
            if "stars" in r["extra"]:
                r["extra"]["starred"] = self.handleStarRespose(request.user.id, r["extra"]["stars"])
            else:
                r["extra"]["starred"] = False
            r["extra"]["stars"] = None

            r["is_editable"] = False
            if r["userID"] == request.user.id:
                r["is_editable"] = True

        return result

    def template_view(self, request):
        # contacts = bulkInsert.contacts
        # for contact in contacts:
        #     ser = self.serializer_class(data=contact)
        #     ser.is_valid(raise_exception=True)
        #     ser.save()


        return render_to_response('Contacts/base.html', {}, context_instance=RequestContext(request))

    def template_view_edit(self, request):
        return render_to_response('Contacts/edit.html', {}, context_instance=RequestContext(request))

    def handleStarRespose(self, userID, stars):
        for s in stars:
            if s["userID"] == userID:
                return s["starred"]
        return False

    def updateStarList(self, userID, stars, value):
        for s in stars:
            if s["userID"] == userID:
                s["starred"] = value
                return stars
        stars.append({
            "userID": userID,
            "starred": value
        })
        return stars

    def create(self, request, *args, **kwargs):
        userID = request.user.id
        request.data["userID"] = userID
        newStart = {
            "userID": request.user.id,
            "starred": request.data['extra']['starred']
        }
        request.data['extra']['stars'] = []
        request.data['extra']['stars'].append(newStart)
        request.data['extra']['starred'] = None
        request.data['extra']['creatorCompanyID'] = self.request.user.current_company.id
        result = super(ContactsViewSet, self).create(request, *args, **kwargs)
        result.data['extra']['starred'] = self.handleStarRespose(userID, result.data['extra']['stars'])
        result.data['extra']['stars'] = None
        return result

    def update(self, request, *args, **kwargs):
        self.get_queryset()
        userID = request.user.id
        contactInstace = self.queryset.get(id=kwargs['id'])

        stars = contactInstace.extra['stars']
        newStars = self.updateStarList(request.user.id, stars, request.data['extra']['starred'])
        request.data['extra']['stars'] = newStars
        request.data['extra']['creatorCompanyID'] = self.request.user.current_company.id
        result = super(ContactsViewSet, self).update(request, *args, **kwargs)
        result.data['extra']['starred'] = self.handleStarRespose(userID, result.data['extra']['stars'])
        result.data['extra']['stars'] = None
        return result


class ContactsGroupsViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = ContactsGroups.objects.all()
    serializer_class = ContactsGroupsSerializer
    pagination_class = DetailsPagination

    # queryset = Contacts.objects.all().order_by("-dateOfPost")

    def create(self, request, *args, **kwargs):
        self.get_queryset()
        userID = request.user.id
        request.data["userID"] = userID
        result = super(ContactsGroupsViewSet, self).create(request, *args, **kwargs)
        return result

    def get_queryset(self):
        self.queryset = ContactsGroups.objects.filter(userID=self.request.user.id)
        return self.queryset

    def list(self, request, *args, **kwargs):
        self.get_queryset()
        result = super(ContactsGroupsViewSet, self).list(request, *args, **kwargs)
        return result

    @detail_route(methods=("get",))
    def getGroups(self, request, *args, **kwargs):
        AllGroups = self.list(request, *args, **kwargs)
        userID = request.user.id
        selectedContactID = kwargs['id']
        GroupsIds = [i["id"] for i in AllGroups.data["results"]]
        checkedGroups = list(ContactsGroupItems.objects.filter(member=selectedContactID))
        checkedGroups = list(ContactsGroupItemsSerializer(instance=z).data for z in checkedGroups)
        for ag in AllGroups.data["results"]:
            ag["checked"] = False
            for cg in checkedGroups:
                if ag["id"] == cg["group"]:
                    ag["checked"] = True
        return AllGroups


class ContactsItemsGroupsViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = ContactsGroupItems.objects.all()
    serializer_class = ContactsGroupItemsSerializer
    pagination_class = DetailsPagination

    # queryset = Contacts.objects.all().order_by("-dateOfPost")

    def create(self, request, *args, **kwargs):
        userID = request.user.id
        request.data["userID"] = userID
        ContactsGroupItems.objects.filter(
            userID=userID,
            group=request.data["group"],
            member=request.data["member"]
        ).delete()
        result = Response({})
        if request.data['checked']:
            request.data.pop("checked")
            result = super(ContactsItemsGroupsViewSet, self).create(request, *args, **kwargs)
        return result
