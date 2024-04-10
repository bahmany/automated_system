from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter



from amspApp.SpecialApps.****Cashflow.pageLoader import PageLoaderApi
from amspApp.SpecialApps.****Cashflow.views.****CashFlowProjectsView import ****CashFlowProjectsViewset
from amspApp.SpecialApps.****Cashflow.views.****CashflowAllDatesView import ****CashflowAllDatesViewset

projects_router = SimpleRouter()
projects_router.register("projects", ****CashFlowProjectsViewset, base_name="news-list")

daily_router = SimpleRouter()
daily_router.register("daily", ****CashflowAllDatesViewset, base_name="news-list")


urlpatterns = patterns('',
                       url(r'^page/base', PageLoaderApi.as_view({"get": "base"})),
                       url(r'^api/v1/', include(projects_router.urls)),
                       url(r'^api/v1/', include(daily_router.urls)),
)

