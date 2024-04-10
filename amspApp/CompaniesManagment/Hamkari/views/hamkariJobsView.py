from asq.initiators import query
from mongoengine import Q
from rest_framework.decorators import list_route
from rest_framework.response import Response

from amspApp.Administrator.Customers.models import UserCustomer
from amspApp.Administrator.Customers.views.CustomerRegistrationView import CustomerRegistrationViewSet
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.permissions.CompanyPermissions import CanCruid
from amspApp.CompaniesManagment.permissions.PermissionChecker import get_permissions
from amspApp.MyProfile.models import Profile, HiddenProfiles
from amspApp.MyProfile.serializers.ProfileSerializer import ProfileSerializer
from amspApp.amspUser.models import MyUser

__author__ = 'mohammad'

from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework_mongoengine import viewsets
from amspApp._Share.ListPagination import DetailsPagination

__author__ = 'mohammad'


class HamkariJobsViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = DetailsPagination
    permission_name = "Can_edit_peoples_to_hire"
    permission_classes = (CanCruid,)

    def get_permissions(self):
        return get_permissions(self, HamkariJobsViewSet)

    def filter_queryset(self, queryset):
        """
        q = search text
        s = search items
        """
        queryparams = self.request.query_params
        qstr = ""
        if "q" in queryparams:
            if queryparams["q"] != "undefine":
                qstr = queryparams["q"]
        qs = []
        if "s" in queryparams:
            if queryparams["s"] != "undefine":
                fields = queryparams["s"].split("___")
                for f in fields:
                    if f != "":
                        if qstr != "":
                            qs.append(Q(**{"extra__job__Shenasnameh__" + f + "__startswith": qstr}))
        andFilter = []
        if "f" in queryparams:
            if queryparams["f"] != "undefine":
                recs = queryparams["f"].split("978547")
                for re in recs:
                    if re != "":
                        andFilter.append(
                            Q(**{
                                re.split("798745")[0].replace("$", "").replace(".", "__"): re.split("798745")[1]
                            })
                        )
                        re.split("798745")

        filters = None
        for q in qs:
            if filters == None:
                filters = q
            else:
                filters = filters | q

        andF = None
        for q in andFilter:
            if andF == None:
                andF = q
            else:
                andF = andF | q

        finalFilter = filters
        if andF:
            if filters and andF:
                finalFilter = filters & andF
            if andF and (not finalFilter):
                finalFilter = andF
            if (not andF) and (finalFilter):
                finalFilter = finalFilter

        if finalFilter:
            queryset = queryset.filter(finalFilter)

        return queryset

    def template_page(self, request, *args, **kwargs):
        return render_to_response("companyManagement/Hamkari/HamkariJobs/base.html", {},
                                  context_instance=RequestContext(self.request))

    def template_page_preview(self, request, *args, **kwargs):
        return render_to_response("Virtual/Profile/Estekhdam/PreviewWithComment.html", {},
                                  context_instance=RequestContext(self.request))

    def getProfiles(self, request, companyID):
        # userIDs = list(PositionsDocument.objects.filter(companyID=companyID).values_list("userID"))
        userIDs = []
        customerID = CustomerRegistrationViewSet().GetCustomerIDFromBilling(request)
        # userIDsRegisteredWithSubdomain
        userIDsRegisteredWithSubdomain = list(UserCustomer.objects.filter(customerID=customerID).order_by("-id").values_list("userID"))
        # converting touple to int !!! i dont know why !
        userIDsRegisteredWithSubdomain = [x[0] for x in userIDsRegisteredWithSubdomain]
        profiles = Profile.objects.filter(
            Q(userID__in=userIDsRegisteredWithSubdomain)).order_by("-dateOfPost")

        profiles = profiles.filter( id__nin = [x["profile"].id for x in HiddenProfiles.objects.filter(companyID = companyID)])
        # profiles = Profile.objects.filter(Q(userID__nin=userIDs)).filter(
        #     Q(userID__in=userIDsRegisteredWithSubdomain)).order_by("-id")
        self.pagination_class.page_size = 50
        return profiles

    def list(self, request, *args, **kwargs):
        CustomerUserID = CustomerRegistrationViewSet().GetUserInstanceFromBilling(request)
        # if not CustomerUserID.id == request.user.id:
        #     return Response({"result": "not found"})
        self.queryset = self.getProfiles(request, kwargs["companyID_id"])
        result = super(HamkariJobsViewSet, self).list(request, *args, **kwargs)

        positionsInstance = list(PositionsDocument.objects.filter(
            # companyID=request.user.current_company_id,
            companyID=700,  # for **** purpose only
            userID__in=[x["userID"] for x in result.data["results"]]
        ))
        for r in result.data["results"]:
            activePositionCount = query(positionsInstance).where(lambda x: x["userID"] == r["userID"]).count()
            if activePositionCount:
                position = query(positionsInstance).where(lambda x: x["userID"] == r["userID"]).to_list()[0]
                r["hasPosition"] = True
                r["positionName"] = position.chartName
                r['profileID'] = None
                r['chartID'] = position.chartName
                r['positionID'] = position.positionID
                r['companyID'] = position.companyID

        users = list(MyUser.objects.filter(id__in = [x["userID"] for x in result.data["results"]]))
        users = [{"username":x.username, "id":x.id} for x in users]
        for r in result.data["results"]:
            r["username"] = query(users).where(lambda x:x["id"] == r["userID"]).to_list()[0]["username"]

        return result




    Education_sortOrder = [{"name": "کاردانی", "value": 1, "contains": 0},
                           {"name": "کارشناسی", "value": 2, "contains": 0},
                           {"name": "کارشناسی ارشد", "value": 3, "contains": 0},
                           {"name": "دکتری", "value": 4, "contains": 0},
                           {"name": "حوزوی", "value": 5, "contains": 0},
                           {"name": "پزشکی", "value": 6, "contains": 0}]

    def getHigherEducation(self, profile):
        if "job" in profile.extra:
            if "Education" in profile.extra["job"]:
                if "items" in profile.extra["job"]["Education"]:
                    sss = 0
                    for f in profile.extra["job"]["Education"]["items"]:
                        for es in self.Education_sortOrder:
                            if f["Education"] == es["name"]:
                                if sss <= es["value"]:
                                    sss = es["value"]
                    for f in profile.extra["job"]["Education"]["items"]:
                        if sss != 0:
                            if self.Education_sortOrder[sss - 1]["name"] == f["Education"]:
                                return f
        return None

    @list_route(methods=["get"])
    def combineListOfEducationWithFinal(self, request):
        profiles = Profile.objects.all()
        test = []
        for p in profiles:
            exp = p.extra
            latestAds = self.getHigherEducation(p)
            if "job" in exp:
                if "Education" in exp["job"]:
                    if "items" in exp["job"]["Education"]:
                        try:
                            if latestAds != None:
                                edut = exp["job"]["Education"].copy()
                                exp["job"]["Education"].update(latestAds)
                                p.update(set__extra=exp)
                                print(exp["job"]["Education"])
                        except:
                            pass

    @list_route(methods=["get"])
    def makeLeftMenuWithStatics(self, request, *args, **kwargs):
        # self.combineListOfEducationWithFinal(request)
        profiles = self.getProfiles(request, kwargs["companyID_id"])
        # jensiat
        self = self
        jens = list(
            profiles.aggregate({"$group": {"_id": "$extra.job.Shenasnameh.Jensiat", "count": {"$sum": 1}},}))
        mazhab = list(
            profiles.aggregate({"$group": {"_id": "$extra.job.Shenasnameh.Mazhab", "count": {"$sum": 1}},}))
        tahol = list(
            profiles.aggregate({"$group": {"_id": "$extra.job.Shenasnameh.Married", "count": {"$sum": 1}},}))
        khedmat = list(
            profiles.aggregate({"$group": {"_id": "$extra.job.Shenasnameh.Soldier", "count": {"$sum": 1}},}))
        tahsilat = list(profiles.aggregate(
            {"$group": {"_id": "$extra.job.Education.LevelofEducation", "count": {"$sum": 1}},}))
        tahsilatLevel = list(profiles.aggregate(
            {"$group": {"_id": "$extra.job.Education.Education", "count": {"$sum": 1}},}))

        tahsilatBranch = list(profiles.aggregate(
            {"$group": {"_id": "$extra.job.Education.SelectedBranch"},}))

        # selected = self.Education_sortOrder[sss]



        # nameOnvan = list(
        # Profile.objects.aggregate({"$group": {"_id": "$extra.job.Job.items.NameOnvan", "count": {"$sum": 1}}, }))

        result = [
            {
                "name": "جنسیت",
                "fieldName": "$extra.job.Shenasnameh.Jensiat",
                "result": jens
            },
            {
                "name": "مذهب",
                "fieldName": "$extra.job.Shenasnameh.Mazhab",
                "result": mazhab
            },
            {
                "name": "تاهل",
                "fieldName": "$extra.job.Shenasnameh.Married",
                "result": tahol
            },
            {
                "name": "نظام وظیفه",
                "fieldName": "$extra.job.Shenasnameh.Soldier",
                "result": khedmat
            },
            {
                "name": "سطح تحصیلات",
                "fieldName": "$extra.job.Education.LevelofEducation",
                "result": tahsilat
            },
            {
                "name": "میزان تحصیلات",
                "fieldName": "$extra.job.Education.Education",
                "result": tahsilatLevel
            },
            {
                "name": "رشته",
                "fieldName": "$extra.job.Education.SelectedBranch",
                "result": tahsilatBranch
            },
            # {
            #     "name": "Education Level",
            #     "fieldName": "$extra.job.Job.items.NameOnvan",
            #     "result": nameOnvan
            # },
        ]

        return Response(result)
