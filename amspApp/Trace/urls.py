from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter

from amspApp.Trace.views.TraceBaseView import TraceFromToViewSet
from amspApp.Trace.views.TraceCategoriesView import TraceCatViewSet
from amspApp.Trace.views.TraceEntryView import TraceEntryViewSet
from amspApp.Trace.views.TraceTypesView import TraceTypesViewSet

trace_fromto_cat_router = SimpleRouter()
trace_fromto_cat_router.register("trace_fromto_cat", TraceCatViewSet, base_name="cardexhamk-list")

trace_fromto_type_router = SimpleRouter()
trace_fromto_type_router.register("trace_type", TraceTypesViewSet, base_name="cardexhamk-list")

trace_fromto_entry_router = SimpleRouter()
trace_fromto_entry_router.register("trace_entry", TraceEntryViewSet, base_name="cardexhamk-list")

urlpatterns = patterns('',

                       url(r'^page/cog_trace_base_cat', TraceCatViewSet.as_view({"get": "template_view"})),
                       url(r'^page/cog_trace_base', TraceFromToViewSet.as_view({"get": "template_view"})),
                       url(r'^page/cog_trace_types', TraceTypesViewSet.as_view({"get": "template_view"})),
                       url(r'^page/cog_trace_entry', TraceEntryViewSet.as_view({"get": "template_view"})),

                       url(r'^api/v1/', include(trace_fromto_cat_router.urls)),
                       url(r'^api/v1/', include(trace_fromto_type_router.urls)),
                       url(r'^api/v1/', include(trace_fromto_entry_router.urls)),

                       )
