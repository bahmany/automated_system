from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter

from amspApp.Sales.views.AdminGoodsProvidersView import AdminTaminDakheliViewSet
from amspApp.Sales.views.CustomerProfileView import CustomerProfileViewSet
from amspApp.Sales.views.CustomerSaleBasket import CustomerSaleBasketViewset
from amspApp.Sales.views.ExitsView import ExitsViewSet, KhoroojViewSet
from amspApp.Sales.views.HavalehForooshView import HavalehForooshViewSet, HavalehForooshConvViewSet
from amspApp.Sales.views.HavalehForooshViewOld import HavalehForooshOldViewSet, HavalehForooshConvOldViewSet
from amspApp.Sales.views.MojoodiGhabeleForooshView import MojoodiGhabeleForooshViewSet
from amspApp.Sales.views.SaleConversationCommentsView import SalesConversationCommentsViewSet
from amspApp.Sales.views.SaleConversationItemsView import SalesConversationItemsViewSet
from amspApp.Sales.views.SaleService import getMojoodiCsv
from amspApp.Sales.views.SalesView import SalesViewSet
from amspApp.Sales.views.TaminProjectDetailsView import TaminProjectDetailsView
from amspApp.Sales.views.TaminProjectView import TaminProjectViewSet
from amspApp.Sales.views.TaminView import TaminViewSet
from amspApp.Sales.views.profile.SalesCustomerProfileSalesRequestsSizesView import \
    SalesCustomerProfileSalesRequestsSizesViewSet

nn = SimpleRouter()
nn.register("salesConv", SalesViewSet, base_name="notify")

nv = SimpleRouter()
nv.register("salesItems", SalesConversationItemsViewSet, base_name="notify")

nc = SimpleRouter()
nc.register("salesComments", SalesConversationCommentsViewSet, base_name="notify")

nPr = SimpleRouter()
nPr.register("salesProjects", TaminProjectViewSet, base_name="notify")

np = SimpleRouter()
np.register("salesProfile", CustomerProfileViewSet, base_name="profile")

nps = SimpleRouter()
nps.register("salesProfileSizes", SalesCustomerProfileSalesRequestsSizesViewSet, base_name="profile")

npBi = SimpleRouter()
npBi.register("saleBasket", CustomerSaleBasketViewset, base_name="profile")

npBa = SimpleRouter()
npBa.register("saleTaminProjectDetail", TaminProjectDetailsView, base_name="profile")

eBa = SimpleRouter()
eBa.register("exits", ExitsViewSet, base_name="profile")



hf = SimpleRouter()
hf.register("havakehForoosh", HavalehForooshViewSet, base_name="profile")

hfc = SimpleRouter()
hfc.register("havakehForooshConv", HavalehForooshConvViewSet, base_name="profile")



hfOld = SimpleRouter()
hfOld.register("havakehForooshOld", HavalehForooshOldViewSet, base_name="profile")

hfcOld = SimpleRouter()
hfcOld.register("havakehForooshConvOld", HavalehForooshConvOldViewSet, base_name="profile")





af = SimpleRouter()
af.register("adminTaminDakheli", AdminTaminDakheliViewSet, base_name="profile")

mgf = SimpleRouter()
mgf.register("mojoodiGhabeleForoosh", MojoodiGhabeleForooshViewSet, base_name="profile")


# --------------------------------------------
khr = SimpleRouter()
khr.register("hamkaranKhorooj", KhoroojViewSet, base_name="havalehforoosh")



# nc = SimpleRouter()
# nc.register("salesProjects", TaminProjectViewSet, base_name="notify")
#
urlpatterns = patterns(

    '',
    url(r'^api/v1/', include(nPr.urls)),
    url(r'^api/v1/', include(nc.urls)),
    url(r'^api/v1/', include(nn.urls)),
    url(r'^api/v1/', include(nv.urls)),
    url(r'^api/v1/', include(np.urls)),
    url(r'^api/v1/', include(nps.urls)),
    url(r'^api/v1/', include(npBi.urls)),
    url(r'^api/v1/', include(eBa.urls)),
    url(r'^api/v1/', include(npBa.urls)),
    url(r'^api/v1/', include(hfOld.urls)),
    url(r'^api/v1/', include(hfcOld.urls)),

    url(r'^api/v1/', include(hf.urls)),
    url(r'^api/v1/', include(hfc.urls)),
    url(r'^api/v1/', include(mgf.urls)),



    url(r'^api/v1/', include(af.urls)),
    url(r'^api/v1/', include(khr.urls)),

    url(r'^api/v1/download_service/21312323556768634523424234/', getMojoodiCsv),

    url(r'^page/showSignBodyPrc', SalesViewSet.as_view({"get": "template_view_showSignBodyPrc"})),

    url(r'^page/KhoroojRep1', SalesViewSet.as_view({"get": "template_view_KhoroojRep1"})),
    url(r'^page/KhoroojDetails', SalesViewSet.as_view({"get": "template_view_Khoroj_Details"})),
    url(r'^page/Khorooj', SalesViewSet.as_view({"get": "template_view_Khoroj"})),

    url(r'^page/MojoodiGhabeleForooshBase', SalesViewSet.as_view({"get": "template_view_MojoodiGhabeleForooshBase"})),

    url(r'^page/MojoodiGhabeleForooshpartial_aniling', SalesViewSet.as_view({"get": "template_view_MojoodiGhabeleForooshpartial_aniling"})),
    url(r'^page/MojoodiGhabeleForooshpartial_nokteh_keifi', SalesViewSet.as_view({"get": "template_view_MojoodiGhabeleForooshpartial_nokteh_keifi"})),
    url(r'^page/MojoodiGhabeleForooshpartial_sefaresh', SalesViewSet.as_view({"get": "template_view_MojoodiGhabeleForooshpartial_sefaresh"})),
    url(r'^page/MojoodiGhabeleForooshpartial_setare_dar', SalesViewSet.as_view({"get": "template_view_MojoodiGhabeleForooshpartial_setare_dar"})),
    url(r'^page/MojoodiGhabeleForooshpartial_tozihat', SalesViewSet.as_view({"get": "template_view_MojoodiGhabeleForooshpartial_tozihat"})),

    url(r'^page/OldKhoroojDetails', SalesViewSet.as_view({"get": "template_view_Old_Khoroj_Details"})),
    url(r'^page/OldKhorooj', SalesViewSet.as_view({"get": "template_view_Old_Khoroj"})),


    url(r'^page/HavalehForooshChange', SalesViewSet.as_view({"get": "template_view_HavalehForooshChange"})),
    url(r'^page/HavalehForooshDetails', SalesViewSet.as_view({"get": "template_view_HavalehForooshDetails"})),
    url(r'^page/HavalehForoosh', SalesViewSet.as_view({"get": "template_view_HavalehForoosh"})),

    url(r'^page/OldHavalehForooshChange', SalesViewSet.as_view({"get": "template_view_OldHavalehForooshChange"})),
    url(r'^page/OldHavalehForooshDetails', SalesViewSet.as_view({"get": "template_view_OldHavalehForooshDetails"})),
    url(r'^page/OldHavalehForoosh', SalesViewSet.as_view({"get": "template_view_OldHavalehForoosh"})),


    url(r'^page/SalesTaminDetails', TaminViewSet.as_view({"get": "template_view_tamin_Details"})),
    url(r'^page/SalesTaminProjects', TaminViewSet.as_view({"get": "template_view_SalesTaminProjects"})),
    url(r'^page/salesTamin', TaminViewSet.as_view({"get": "template_view_base"})),
    url(r'^page/AdminTaminDakheliDetails', TaminViewSet.as_view({"get": "template_view_AdminTaminDakheliDetails"})),
    url(r'^page/AdminTaminDakheli', TaminViewSet.as_view({"get": "template_view_AdminTaminDakheli"})),


    url(r'^page/saleaddbasket', SalesViewSet.as_view({"get": "template_view_saleaddbasket"})),
    url(r'^page/SendSMS', SalesViewSet.as_view({"get": "template_view_SendSMS"})),

    url(r'^page/SalesProfilePhones', SalesViewSet.as_view({"get": "template_view_SalesProfilePhones"})),
    url(r'^page/salesAddCustomerProfile', SalesViewSet.as_view({"get": "template_view_sales_customer_profile_modal"})),
    url(r'^page/salesKarshenasiAddNew', SalesViewSet.as_view({"get": "template_view_salesKarshenasiAddNew_modal"})),
    url(r'^page/salesTataabogh', SalesViewSet.as_view({"get": "template_view_sales_tataabogh"})),
    url(r'^page/salesConversationsItems', SalesViewSet.as_view({"get": "template_view_sales_conversations_items"})),
    url(r'^page/salesConversationsAddNew', SalesViewSet.as_view({"get": "template_view_sales_conversations_add_new"})),

    url(r'^page/salesConversations', SalesViewSet.as_view({"get": "template_view_sales_conversations"})),
    url(r'^page/salesConv', SalesViewSet.as_view({"get": "template_view_saleConv"})),
    url(r'^page/salesMojoodi', SalesViewSet.as_view({"get": "template_view_salesMojoodi"})),
    url(r'^page/SalesProfileDetails', SalesViewSet.as_view({"get": "template_view_SalesProfileDetails"})),
    url(r'^page/SalesProfile', SalesViewSet.as_view({"get": "template_view_SalesProfile"})),
    url(r'^page/SalesCustomerTahiliDetails', SalesViewSet.as_view({"get": "template_view_SalesCustomerTahiliDetails"})),
    url(r'^page/SalesCustomerTahili', SalesViewSet.as_view({"get": "template_view_SalesCustomerTahili"})),
    url(r'^page/KarshenasiTahili', SalesViewSet.as_view({"get": "template_view_KarshenasiTahili"})),
    url(r'^page/Karshenasi', SalesViewSet.as_view({"get": "template_view_Karshenasi"})),
    url(r'^page/sales_report_base', SalesViewSet.as_view({"get": "template_view_sales_report_base"})),
    url(r'^page/sales_report_trace_havaleh_foroosh', SalesViewSet.as_view({"get": "template_view_sales_report_trace_havaleh_foroosh"})),
    url(r'^page/sales', SalesViewSet.as_view({"get": "template_view"})),
    url(r'^page/get_pishfactor_base', SalesViewSet.as_view({"get": "template_view_pishfactor_base"})),

)

