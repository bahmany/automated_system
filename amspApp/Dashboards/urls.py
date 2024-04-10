# coding=utf-8
from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter

from amspApp.Dashboards.Registeration.FirstReg import FirstRegView
from amspApp.Dashboards.Registeration.FirstViewset import FirstregViewset
from amspApp.Dashboards.Registeration.SecondReg import SecondRegView
from amspApp.Dashboards.Supply.views.GoodsSupplyView import GoodsProvidersViewSet, GoodsProvidersApi
from amspApp.Dashboards.views.homeView import Home
from amspApp.Dashboards.Login.loginView import LoginView

firstreg_router = SimpleRouter()
firstreg_router.register("firstreg", FirstregViewset, base_name="news-list")

supp = SimpleRouter()
supp.register("supp", GoodsProvidersViewSet, base_name="news-list")

urlpatterns = patterns('',

                       # url(r'api/v1/firstRegister/', FirstRegView.as_view),

                       url(r'^api/v1/', include(firstreg_router.urls)),

                       url(r'^api/v1/save_supply/', GoodsProvidersApi.as_view({'post': 'post'})),
                       url(r'^api/v1/sp_save_supply/', GoodsProvidersApi.as_view({'post': 'post_sp'})),
                       url(r'^api/v1/get_ozviat_code/', GoodsProvidersApi.as_view({'get': 'get_ozviat_code'})),
                       url(r'^api/v1/get_supply/', GoodsProvidersApi.as_view({'get': 'get'})),

                       url(r'^page/base', Home.as_view({'get': 'base'})),
                       url(r'^page/home', Home.as_view({'get': 'home'})),
                       url(r'^page/profile', Home.as_view({'get': 'profile'})),
                       url(r'^page/login', LoginView.as_view({'get': 'loginForm'})),
                       url(r'^page/firstreg', FirstRegView.as_view({'get': 'firstregForm'})),
                       url(r'^page/forgetPass', FirstRegView.as_view({'get': 'forgetPassForm'})),
                       url(r'^page/secondreg', SecondRegView.as_view({'get': 'secondregForm'})),
                       url(r'^page/baseSupply', SecondRegView.as_view({'get': 'baseSupply'})),
                       url(r'^page/imageDialog', SecondRegView.as_view({'get': 'imageDialog'})),
                       url(r'^page/OpenCateg', SecondRegView.as_view({'get': 'OpenCateg'})),
                       url(r'^page/supplyItems/(?P<pk>\d+)/$', SecondRegView.as_view({'get': 'supplyItems'})),
                       url(r'^', Home.as_view({'get': 'index'}))

                       )
