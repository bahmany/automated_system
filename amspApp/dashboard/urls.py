from django.conf.urls import patterns, include, url
from amspApp.dashboard.views import HomeView

urlpatterns = patterns('',

                       url(r'^our/home', HomeView.Home.as_view({'get': 'home'})),

                       url(r'^page/dashboard/Statics', HomeView.Home.as_view({"get": "template_dash_static_view"})),

                       url(r'^scripts/directives/topnav/', HomeView.Home.as_view({'get': 'topnav'})),
                       url(r'^scripts/directives/select_position_directive/', HomeView.Home.as_view({'get': 'selectPosition'})),
                       url(r'^scripts/directives/select_chart_directive/', HomeView.Home.as_view({'get': 'selectChart'})),

                       url(r'^scripts/directives/menu/', HomeView.Home.as_view({'get': 'generateSideBar'})),
                       url(r'^scripts/directives/sidebar/', HomeView.Home.as_view({'get': 'sidebar'})),

                       url(r'^api/v1/forced/getForceNotification/', HomeView.Home.as_view({'get': 'addSomeToProfile'})),

                       url(r'^api/v1/forced/profileSeenFirstTime/', HomeView.Home.as_view({'get': 'profileSeenFirstTime'})),
                       url(r'^api/v1/forced/getDashboardHelp/', HomeView.Home.as_view({'get': 'getDashboardHelp'})),
                       url(r'^api/v1/forced/getDashboard/', HomeView.Home.as_view({'get': 'getDashboard'})),
                       url(r'^api/v1/forced/setDashboard/', HomeView.Home.as_view({'post': 'setDashboard'})),
                       url(r'^api/v1/forced/setStaticDashboard/', HomeView.Home.as_view({'post': 'setStaticDashboard'})),

)
