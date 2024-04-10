from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter

from amspApp.Material.pageLoader import PageLoaderApi
from amspApp.Material.views.BarcodesViewSet import BarcodesViewSet
from amspApp.Material.views.MaterialConvSaleView import MaterialConvSaleViewSet
from amspApp.Material.views.WarehousesViewSet import WarehousesViewSet

nn = SimpleRouter()
nn.register("warehouse", WarehousesViewSet, base_name="notify")

mm = SimpleRouter()
mm.register("barcodes", BarcodesViewSet, base_name="notify")

mc = SimpleRouter()
mc.register("materialconvsale", MaterialConvSaleViewSet, base_name="notify")

urlpatterns = patterns(
    '',
    url(r'^api/v1/', include(nn.urls)),
    url(r'^api/v1/', include(mm.urls)),
    url(r'^api/v1/', include(mc.urls)),

    url(r'^Material/page/materialbaskol/', PageLoaderApi.as_view({"get": "template_materialbaskol"})),
    url(r'^Material/page/materiallocations/', PageLoaderApi.as_view({"get": "template_locations"})),
    url(r'^Material/page/materialbase/', PageLoaderApi.as_view({"get": "template_view_read"})),
    url(r'^Material/page/popupMasraf/', PageLoaderApi.as_view({"get": "template_popupMasraf"})),
    url(r'^Material/page/popupBaskol/', PageLoaderApi.as_view({"get": "template_popupBaskol"})),
    url(r'^Material/page/materialVoroodKhrooj/', PageLoaderApi.as_view({"get": "template_materialVoroodKhrooj"})),
    url(r'^Material/page/materialBarcodeList/', PageLoaderApi.as_view({"get": "template_materialBarcodeList"})),
    url(r'^Material/page/materialBarnameTolid/', PageLoaderApi.as_view({"get": "template_materialBarnameTolid"})),
    url(r'^Material/page/materialBarnameBase/', PageLoaderApi.as_view({"get": "template_materialBarnameBase"})),
    url(r'^Material/page/materialBasket/', PageLoaderApi.as_view({"get": "template_materialBasket"})),
    url(r'^Material/page/fromBaskolToAnbar/', PageLoaderApi.as_view({"get": "template_materialfromBaskolToAnbar"})),
    url(r'^Material/page/fromQCBlackplate/', PageLoaderApi.as_view({"get": "template_fromQCBlackplate"})),
    url(r'^Material/page/tolidSaleConvSaleItem/', PageLoaderApi.as_view({"get": "template_tolidSaleConvSaleItem"})),
    url(r'^Material/page/tolidSaleConvSale/', PageLoaderApi.as_view({"get": "template_tolidSaleConvSale"})),
    url(r'^Material/page/tolidSaleConv/', PageLoaderApi.as_view({"get": "template_tolidSaleConv"})),
    url(r'^Material/page/materialReportBase/', PageLoaderApi.as_view({"get": "template_report_base"})),
    url(r'^Material/page/materialReport1/', PageLoaderApi.as_view({"get": "template_report_1"})),
    url(r'^Material/page/materialReport2/', PageLoaderApi.as_view({"get": "template_report_2"})),

)
