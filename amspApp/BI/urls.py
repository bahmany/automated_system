from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter

from amspApp.BI.pageloader import PageLoaderApi
from amspApp.BI.views.BIChartView import BIChartViewSet
from amspApp.BI.views.BIDashboardView import BIDashboardPageViewSet
from amspApp.BI.views.BIDatasourcesView import BIDatasourcesViewSet
from amspApp.BI.views.BIGroupsView import BIGroupsViewSet
from amspApp.BI.views.BIMenuView import BIMenuViewSet, BIMenuItemsViewSet
from amspApp.BI.views.BISqls import BISqlsViewSet

mc = SimpleRouter()
mc.register("bi_group", BIGroupsViewSet, base_name="notify")

mci = SimpleRouter()
mci.register("bi_dashboard_page", BIDashboardPageViewSet, base_name="notify")

mcp = SimpleRouter()
mcp.register("bi_chart", BIChartViewSet, base_name="notify")

mcd = SimpleRouter()
mcd.register("bi_datasources", BIDatasourcesViewSet, base_name="notify")

mcs = SimpleRouter()
mcs.register("bi_sqls", BISqlsViewSet, base_name="notify")

mcb = SimpleRouter()
mcb.register("bi_menus", BIMenuViewSet, base_name="notify")

mcbi = SimpleRouter()
mcbi.register("bi_menus_items", BIMenuItemsViewSet, base_name="notify")


urlpatterns = patterns(
    '',
    url(r'^page/bibasepage', PageLoaderApi.as_view({"get": "template_bibasepage"})),
    url(r'^page/bigroupspartialmembers', PageLoaderApi.as_view({"get": "template_bigroupspartialmembers"})),

    url(r'^page/bigroups', PageLoaderApi.as_view({"get": "template_bigroups"})),

    url(r'^page/bidashboardpagesdashboard', PageLoaderApi.as_view({"get": "template_bidashboardpagesdashboard"})),
    url(r'^page/bidashboardpages', PageLoaderApi.as_view({"get": "template_bidashboardpages"})),
    url(r'^page/bipages', PageLoaderApi.as_view({"get": "template_bipages"})),
    url(r'^page/bipage', PageLoaderApi.as_view({"get": "template_bipage"})),

    url(r'^page/bichartdesign', PageLoaderApi.as_view({"get": "template_bichartdesign"})),
    url(r'^page/bicharts', PageLoaderApi.as_view({"get": "template_bicharts"})),

    url(r'^page/bidatasourcesmodal', PageLoaderApi.as_view({"get": "template_bidatasourcesmodal"})),
    url(r'^page/bidatasourcesdesign', PageLoaderApi.as_view({"get": "template_bidatasourcesdesign"})),
    url(r'^page/bidatasources', PageLoaderApi.as_view({"get": "template_bidatasources"})),

    url(r'^page/bisqls', PageLoaderApi.as_view({"get": "template_bisqlsbase"})),
    url(r'^page/bisql', PageLoaderApi.as_view({"get": "template_bisql"})),

    url(r'^page/bimenuspartialitems', PageLoaderApi.as_view({"get": "template_bimenuspartialitems"})),
    url(r'^page/bimenuspartialmembersusers', PageLoaderApi.as_view({"get": "template_bimenuspartialmembersusers"})),
    url(r'^page/bimenuspartialmembers', PageLoaderApi.as_view({"get": "template_bimenuspartialmembers"})),
    url(r'^page/bimenus', PageLoaderApi.as_view({"get": "template_bimenus"})),

    url(r'^page/bi_sample_page_for_ceo', PageLoaderApi.as_view({"get": "template_bi_sample_page_for_ceo"})),
    url(r'^page/amareroozaneh', PageLoaderApi.as_view({"get": "template_amareroozaneh"})),

    url(r'^api/v1/', include(mc.urls)),
    url(r'^api/v1/', include(mci.urls)),
    url(r'^api/v1/', include(mcp.urls)),
    url(r'^api/v1/', include(mcbi.urls)),
    url(r'^api/v1/', include(mcd.urls)),
    url(r'^api/v1/', include(mcs.urls)),
    url(r'^api/v1/', include(mcb.urls)),

)
