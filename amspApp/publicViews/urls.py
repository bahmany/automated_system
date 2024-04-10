from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter, Route, DynamicDetailRoute
from rest_framework_nested.routers import NestedSimpleRouter
from amspApp.publicViews.SelectMembers.views.SelectMembersView import SelectMembersViewSet



SearchSelectMember_router = SimpleRouter()
SearchSelectMember_router.register("members", SelectMembersViewSet, base_name="SelectMember")




urlpatterns = patterns(
    '',
    url(r'^page/public/selectmember', SelectMembersViewSet.as_view({"get":"template_view"})),
    url(r'^api/v1/select/', include(SearchSelectMember_router.urls)),




)