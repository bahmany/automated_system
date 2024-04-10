from rest_framework_mongoengine import viewsets

from amspApp.ControlProject.permissions.ControlProjectBase import IsOwnerOrReadOnly_CostCol
from amspApp.Infrustructures.Classes.MongoEngineSearchFilterBackend import MongoSearchFilter, FilterCompanyID
from amspApp.Sales.models import SaleCurrentBasket
from amspApp.Sales.serializers.SaleConversationSerializer import SaleCustomerSaleBasket
from amspApp.Sales.views.SalesView import SalesViewSet
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class CustomerSaleBasketViewset(viewsets.ModelViewSet):
    pagination_class = DetailsPagination
    lookup_field = "id"
    serializer_class = SaleCustomerSaleBasket
    queryset = SaleCurrentBasket.objects.all().filter(transfered = False).order_by('-id')
    permission_classes = (IsOwnerOrReadOnly_CostCol,)
    filter_backends = (MongoSearchFilter, FilterCompanyID)
    # search_fields = ("name", "hamkaranCode", "desc")

    def checkPerm(self, req):
        if req.user.groups.filter(name__contains="foroosh").count() == 0:
            raise Exception("مجوز دسترسی ندارید")

    def initialize_request(self, request, *args, **kwargs):
        self.checkPerm(request)
        return super(CustomerSaleBasketViewset, self).initialize_request(request, *args, **kwargs)

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = posiIns.positionID
            request.data["companyID"] = posiIns.companyID
            isAvailable = SalesViewSet().isPartCodeAvailable(request.data["desc"]["itemID"], request.data["desc"]["amount"])
            if not isAvailable:
                raise Exception("بیش از موجودی")
        return super(CustomerSaleBasketViewset, self).initial(request, *args, **kwargs)


    def get_queryset(self):
        posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(self.request)
        self.queryset = self.queryset.filter(positionID = posInstance.positionID)
        return super(CustomerSaleBasketViewset, self).get_queryset()

    def list(self, request, *args, **kwargs):
        self.pagination_class.page_size = 50
        result = super(CustomerSaleBasketViewset, self).list(request, *args, **kwargs)
        return result
