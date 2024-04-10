from __future__ import unicode_literals

from asq.initiators import query
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils import six
from mongoengine import Q
from rest_framework.compat import django_filters, guardian, get_model_name
from rest_framework.filters import BaseFilterBackend
from rest_framework.settings import api_settings
from functools import reduce
import operator

from amspApp.MyProfile.models import Profile
from amspApp.Sales.models import SalesCustomerProfile
from amspApp.amspUser.models import MyUser


class MongoSearchFilter(BaseFilterBackend):
    # The URL query parameter used for the search.
    search_param = api_settings.SEARCH_PARAM

    def get_search_terms(self, request):
        """
        Search terms are set by a ?search=... query parameter,
        and may be comma and/or whitespace delimited.
        """
        params = request.query_params.get(self.search_param, '')
        return params.replace(',', ' ').split()

    def construct_search(self, field_name):
        if field_name.startswith('^'):
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__iexact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__search" % field_name[1:]
        else:
            return "%s__icontains" % field_name

    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, 'search_fields', None)

        if not search_fields:
            return queryset

        orm_lookups = [self.construct_search(six.text_type(search_field))
                       for search_field in search_fields]

        for search_term in self.get_search_terms(request):
            or_queries = [Q(**{orm_lookup: search_term})
                          for orm_lookup in orm_lookups]
            queryset = queryset.filter(reduce(operator.or_, or_queries))

        return queryset


class FilterCompanyID(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(Q(companyID=request.user.current_company_id))


class FilterTitle(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'q' in request.query_params:
            return queryset.filter(Q(title__contains=request.query_params["q"]))
        else:
            return queryset


class FilterName(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'q' in request.query_params:
            return queryset.filter(Q(name__contains=request.query_params["q"]))
        else:
            return queryset


class FilterDataTables(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        searchItems = [s for s in list(request.query_params.keys()) if "earch" in s and "earchable" not in s]
        searchFields = [s for s in list(request.query_params.keys()) if "mDataProp" in s]

        # mapping fields
        searchList = []
        for si in searchItems:
            for sf in searchFields:
                if len(si.split("_")) == 2:
                    if si.split("_")[1] == sf.split("_")[1]:
                        for f in [ss for ss in list(request.query_params.keys()) if "earchable" in ss]:
                            # if request.query_params:
                            dt = {
                                "base": si,
                                "value": request.query_params.get(si),
                                "fieldname": request.query_params.get(sf)
                            }
                            searchList.append(dt)
        finalSearchList = []
        for s in [s for s in list(request.query_params.keys()) if "earchable" in s]:
            for ss in searchList:
                if s.split("_")[1] == ss["base"].split("_")[1]:
                    if request.query_params[s] == "true":
                        finalSearchList.append(ss)
                        break

        if "sSearch" in request.query_params:
            for s in searchList:
                s["value"] = request.query_params.get("sSearch")

        # casting
        for r in finalSearchList:
            if view.datatablesTypes.get(r["fieldname"]):
                r["fieldtype"] = view.datatablesTypes.get(r["fieldname"])

        # generating search mongo
        qlist = []
        for s in finalSearchList:
            if s["fieldname"] == "profileLink.name":
                uss = SalesCustomerProfile.objects.filter(
                    Q(name__icontains=s.get("value", "")) | Q(name__icontains=s.get("value", "")))
                uss = [str(x.id) for x in uss]
                qlist.append(Q(profileLink__in=uss))
            elif s["fieldname"] == "id":
                pass
            else:
                if s.get("fieldtype") == "int":
                    if s["value"].isdigit():
                        s["fieldname"] = s["fieldname"].replace(".", "__")
                        qlist.append(Q(**{s["fieldname"]: int(s["value"])}))
                else:
                    s["fieldname"] = s["fieldname"].replace(".", "__") + "__icontains"
                    qlist.append(Q(**{s["fieldname"]: s["value"]}))
        blist = qlist.pop() if len(qlist) > 0 else []
        for q in qlist:
            blist |= q

        # sorting
        sortItems = [s for s in list(request.query_params.keys()) if "ort" in s and 'able' not in s]
        sortFields = [s for s in list(request.query_params.keys()) if "ort" in s and 'able' in s]
        sortList = []
        for si in sortFields:
            if request.query_params.get(si) == 'true':
                sortList.append({
                    'fieldname': request.query_params.get("mDataProp_" + si.split("_")[1]),
                    'fieldIndex': int(si.split("_")[1]),
                    'sorting': request.query_params.get('iSortCol_0') == si.split("_")[1],
                    'direction': '' if request.query_params.get('sSortDir_0') == "asc" else '-'
                })

        qq = query(sortList).where(lambda x: x['sorting'] == True).to_list()
        sortField = qq[0] if len(qq) > 0 else {
            "fieldname": "id",
            "direction": "_"
        }
        if sortField["fieldname"] == 'profileLink.name':
            sortField["fieldname"] = "id"
            sortField["direction"] = "-"

        return queryset.filter(blist).order_by(sortField['direction'] + sortField['fieldname'].replace('.', "__"))


class FilterHamkriRegisteredPerson(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'q' in request.query_params:
            if request.query_params["q"] == "":
                return queryset
            """ 
            quering profile names
            """
            usernames = MyUser.objects.filter(username__contains=request.query_params["q"])
            emails = MyUser.objects.filter(email__contains=request.query_params["q"])
            profiles = Profile.objects.filter(extra__Name__contains=request.query_params["q"])
            usernames = [x.id for x in usernames]
            emails = [x.id for x in emails]
            profiles = [x.userID for x in profiles]
            all = usernames + emails + profiles

            return queryset.filter(Q(userID__in=all))
        else:
            return queryset
