from django.conf.urls import patterns, url, include

from amspApp.SpecialApps.****Cashflow import urls as ****CashflowUrl
# news_router = SimpleRouter()
# news_router.register("news", NewsViewSet, base_name="news-list")
from amspApp.SpecialApps.pageLoader import PageLoaderApi

urlpatterns = patterns('',

                       url(r'^****Cashflow/', include(****CashflowUrl)),

                       url(r'^page/base', PageLoaderApi.as_view({"get": "base"})),
                       url(r'^page/home', PageLoaderApi.as_view({"get": "home"})),
                       url(r'^page/dash', PageLoaderApi.as_view({"get": "dash"})),

                       url(r'', PageLoaderApi.as_view({"get": "index"})),
                       # url(r'^api/v1/', include(news_router.urls)),
                       )
