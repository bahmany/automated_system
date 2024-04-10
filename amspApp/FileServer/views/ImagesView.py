






from mongoengine import Q
from rest_framework_mongoengine import viewsets

from amspApp.FileServer.models import File
from amspApp.FileServer.permissions.CanCrudFiles import CanCruidFiles
from amspApp.FileServer.serializers.FileSerializer import ImageSerializer
from amspApp._Share.ListPagination import DetailsPagination


class ImagesViewSet(viewsets.ModelViewSet):
    pagination_class = DetailsPagination
    lookup_field = "id"
    serializer_class = ImageSerializer
    queryset = File.objects.filter((Q(originalFileName__contains=".jpg") | Q(originalFileName__contains=".png") | Q(
        originalFileName__contains=".gif")) & Q(originalFileName__not__contains="GeneratedSign")).order_by("-dateOfPost")
    permission_classes = (CanCruidFiles,)
    # filter_backends = (MongoSearchFilter, FilterCompanyID, OrderingFilter)
    search_fields = ("originalFileName",)


    def get_queryset(self):
        if self.request.query_params.get("t"):
            self.queryset = self.queryset.filter(decodedFileName__contains = self.request.query_params.get("t"))
            self.queryset = self.queryset.filter(userID = self.request.user.id)
        return super(ImagesViewSet, self).get_queryset()

    # def list(self, request, *args, **kwargs):
    #     result = super(ImagesViewSet, self).list(request, *args, **kwargs)
    #     for r in result.data.results:



