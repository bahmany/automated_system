from django.conf.urls import patterns, include, url
from rest_framework import routers

from amspApp import views
from amspApp.amspUser.views import UserView
from amspApp.amspUser.views import GroupView
from amspApp.amspUser.views import PermissionView
from amspApp.amspUser.views.UserView import LoginView, LoginViewset

router = routers.SimpleRouter()
router.register(r'users', UserView.UserViewSet, base_name="myuser")
router.register(r'groups', GroupView.GroupViewSet)



# routerForget = routers.SimpleRouter()
# routerForget.register(r'forgetpass', UserView.ForgetPassView, base_name="ForgetPassword")

routerReset = routers.SimpleRouter()
routerReset.register(r'resetpass', UserView.ResetPassView, base_name="ResetPassword")



urlpatterns = patterns(
    '',
    # ... URLs


    url(r'^login', LoginViewset.as_view({'get': 'getTemplate'}), name="loginviewset"),
    # url(r'^page/loginout', LoginView.login),
    # url(r'^page/signup', LoginView.signup),
    # url(r'^page/forget', LoginView.forget),


    url(r'^api/v1/', include(router.urls)),
    url(r'^myapi/users/', UserView.UserViewSet.as_view({'get': 'list'}),name='UserViewList'),

    # url(r'^myapi/', include(routerForget.urls)),
    url(r'^myapi/', include(routerReset.urls)),

    url(r'^myapi/groups/', GroupView.GroupViewSet.as_view({'get': 'list'}),name='GroupViewList'),
    url(r'^myapi/permission/', PermissionView.PermissionViewSet.as_view({'get': 'list'}),name='PermissionViewList'),

    url(r'^api/v1/auth/login/$', UserView.LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/$', views._logout, name='logout'),


)