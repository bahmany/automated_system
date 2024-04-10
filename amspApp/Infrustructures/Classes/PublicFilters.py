import django_filters
from mongoengine import Q

from amspApp.CompaniesManagment.Positions.models import PositionsDocument

__author__ = 'mohammad'
#
#
# def searcTxt(queryset,txt) :
#     queryest.

class QuerySetFilter():
    def __init__(self):
        pass
    def filter(self, querySet,kwargs):
        # amir = querySet._collection_obj.find({"$query": {
        #     "$text": {"$search": 'ce'},}})
        if not 'q' in kwargs.keys():
            return querySet
        if kwargs["q"] == "":
            return querySet
        if kwargs["q"] == "undefined":
            return querySet
        return querySet.filter(Q(profileName__contains = kwargs["q"]) | Q(chartName__contains = kwargs["q"]) )


class QuerySetFilterInMysql():

    searchFields = []
    def __init__(self, searchFieldsName):
        self.searchFields = searchFieldsName
        pass
    def filter(self, querySet,kwargs):
        # amir = querySet._collection_obj.find({"$query": {
        #     "$text": {"$search": 'ce'},}})
        if not 'q' in kwargs.keys():
            return querySet
        if kwargs["q"] == "":
            return querySet
        if kwargs["q"] == "undefined":
            return querySet
        sear = {}
        for s in self.searchFields:
            sear["%s__icontains" % s] =kwargs["q"]
        return querySet.filter(**sear)



