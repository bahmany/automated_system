from rest_framework_mongoengine import viewsets
from amspApp._Share.ListPagination import DetailsPagination

__author__ = 'mohammad'


class InboxListViewSet(viewsets.ModelViewSet):
    pagination_class = DetailsPagination
    lookup_field = "id"
    serializer_class = InboxSerializer



