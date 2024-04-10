from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from amspApp.CompaniesManagment.Hamkari.models import RequestHamkari
from amspApp.CompaniesManagment.Hamkari.serializers.HamkariSerializer import RequestHamkariSerializer
from amspApp.CompaniesManagment.permissions.CompanyPermissions import CanCruid
from amspApp.Infrustructures.Classes.MongoEngineSearchFilterBackend import MongoSearchFilter, FilterName, \
    FilterHamkriRegisteredPerson
from amspApp.MyProfile.models import Profile
from amspApp.MyProfile.serializers.ProfileSerializer import ProfileSerializer
from amspApp._Share.ListPagination import ListPagination, DetailsPagination
from amspApp.amspUser.models import MyUser


class HamkariRequestHamkariViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = RequestHamkari.objects.all().order_by("-id")
    serializer_class = RequestHamkariSerializer
    pagination_class = DetailsPagination
    filter_backends = (MongoSearchFilter, FilterHamkriRegisteredPerson)
    # permission_name = "cruider"
    # permission_classes = (CanCruid,)


    def get_queryset(self):
        self.queryset = self.queryset.filter(jobID = self.kwargs['hamkariID_id'])
        return self.queryset


    def list(self, request, *args, **kwargs):
        result = super(HamkariRequestHamkariViewSet, self).list(request, *args, **kwargs)
        for r in result.data["results"]:
            profile = Profile.objects.filter(userID = r["userID"])
            user = MyUser.objects.get(id = r["userID"])
            r["profile"] = None
            if profile.count() > 0:
                profile = profile[0]
                r["profile"] = ProfileSerializer(instance=profile).data
                r["username"] = user.username
                r["email"] = user.email
        return result


    @list_route(methods=["post"])
    def Seen(self, request, *args, **kwargs):
        instance = self.queryset.get(id = request.data['invID'])
        instance = Profile.objects.get(userID = instance.userID)
        seen = False
        if "seen" in instance.extra:
            seen = instance.extra["seen"]
        instance.update(extra__seen = not seen)
        return Response({})

    @list_route(methods=["post"])
    def Fail(self, request, *args, **kwargs):
        instance = self.queryset.get(id = request.data['invID'])
        instance = Profile.objects.get(userID = instance.userID)
        fail = False
        if "fail" in instance.extra:
            fail = instance.extra["fail"]
        instance.update(extra__fail = not fail)
        return Response({})

    @list_route(methods=["post"])
    def Accept(self, request, *args, **kwargs):
        instance = self.queryset.get(id = request.data['invID'])
        instance = Profile.objects.get(userID = instance.userID)
        accept = False
        if "accept" in instance.extra:
            accept = instance.extra["accept"]
        instance.update(extra__accept= not accept)

        enableLogin = False
        if "isAllowed" in instance.extra:
            enableLogin = instance.extra["isAllowed"]
        instance.update(extra__isAllowed=not enableLogin)

        return Response({})
