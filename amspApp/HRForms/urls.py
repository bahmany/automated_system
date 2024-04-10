# from django.conf.urls import patterns, url
# from dms.HRForms import views
#
# __author__ = 'mohammad'
#
# urlpatterns = patterns('',
#                        url(r'^forms/form/$', views.Form, name='Add New Contact'),
#                        url(r'^forms/post/$', views.Post, name='Add New Contact'),
#                        url(r'^forms/remove/$', views.Remove, name='Add New Contact'),
#                        url(r'^forms/toggle/$', views.Toggle, name='Add New Contact'),
#                        # url(r'^remove-file/$', views.RemoveFile, name='Add New Contact'),
#                        url(r'^forms/get-one/$', views.GetOne, name='Add New Contact'),
#                        url(r'^forms/find-by/$', views.FindBy, name='Add New Contact'),
#                        url(r'^forms/get-table/$', views.GetTable, name='Add New Contact'),
#
# )


from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter, Route, DynamicDetailRoute


letterInboxFolder_router = SimpleRouter()
letterInboxFolder_router.register("hrForms", InboxFolderViewset, base_name="InboxFolderPage")
