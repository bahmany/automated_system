from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.decorators import list_route, detail_route
from rest_framework_mongoengine import viewsets

from amspApp.Trace.models import TraceTypes
from amspApp.Trace.serializers.TraceSerializers import TraceTypesSerializer
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class TraceTypesViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = TraceTypes.objects.all().order_by("-id")
    serializer_class = TraceTypesSerializer
    pagination_class = DetailsPagination
    pagination_class.page_size = 100

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = posiIns.positionID
        return super(TraceTypesViewSet, self).initial(request, *args, **kwargs)

    # @list_route(methods=["post"])
    # def updateRow(self, request, *args, **kwargs):
    #     data = request.data
    #     changed = False
    #     self.queryset.delete()
    #     for d in data:
    #         if d.get('sl') and d.get('gl') and d.get('markazeTashim') and d.get('percent'):
    #             ser = self.serializer_class(
    #                 data=d
    #             )
    #             ser.is_valid(raise_exception=True)
    #             ser.save()
    #             changed = True
    #     return Response({"msg": changed})

    def list(self, request, *args, **kwargs):
        self.serializer_class.Meta.depth = 2

        return super(TraceTypesViewSet, self).list(request, *args, **kwargs)

    @detail_route(methods=["GET"])
    def ret(self, request, *args, **kwargs):
        self.serializer_class.Meta.depth = 1
        rrr = self.retrieve(request, *args, **kwargs)
        return rrr

    def retrieve(self, request, *args, **kwargs):
        # self.serializer_class.Meta.depth = 1
        return super(TraceTypesViewSet, self).retrieve(request, *args, **kwargs)

    def template_view(self, request):
        return render_to_response('Trace/Types/base.html', {}, context_instance=RequestContext(request))
