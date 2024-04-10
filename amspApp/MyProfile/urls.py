from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter, Route, DynamicDetailRoute
from amspApp.MyProfile.viewes.PostsView import PostsViewset
from amspApp.MyProfile.viewes.ProfileManagmentView import ProfileManagmentViewSet


profile_router = SimpleRouter()
profile_router.register("profile", ProfileManagmentViewSet, base_name="ProfilePage")

posts_router = SimpleRouter()
posts_router.register("posts", PostsViewset, base_name="PostsPage")

urlpatterns = patterns(
    '',
    url(r'^api/v1/', include(profile_router.urls)),
    url(r'^api/v1/', include(posts_router.urls)),

    url(r'^page/myProfile', ProfileManagmentViewSet.as_view({"get": "template_view"})),

    url(r'^page/dashboardSettings', ProfileManagmentViewSet.as_view({"get": "template_view_dashboard_settings"}))


)