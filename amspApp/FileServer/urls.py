from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter, Route
from amspApp.FileServer.views.FileFolderItemsView import FileFolderItemsViewset
from amspApp.FileServer.views.FileFoldersView import FileFoldersViewset
from amspApp.FileServer.views.FileManagerApiView import FileManagerApiView
from amspApp.FileServer.views.FileUploadView import FileUploadViewSet, FileUploaderTemplate, FileAttsViewset, \
    FileManagerTemplate
from rest_framework_nested import routers as _routers

from amspApp.FileServer.views.ImagesView import ImagesViewSet

__author__ = 'mohammad'

folder_router = SimpleRouter()
folder_router.register("folders", FileFoldersViewset, base_name="folders-list")


url_file_folder = _routers.NestedSimpleRouter(folder_router, r"folders", lookup="folder")
url_file_folder.register(r'items', FileFolderItemsViewset, base_name="fileFolderItems-list")

url_atts_folder = SimpleRouter()
url_atts_folder.register(r'atts', FileAttsViewset, base_name="fileFolderItems-list")

url_images = SimpleRouter()
url_images.register(r'images', ImagesViewSet, base_name="fileFolderItems-list")


# url_manager = SimpleRouter()
# url_manager .register(r'manager', FileManagerApiView.as_view(), base_name="fileFolderItems-list")






urlpatterns = patterns(
    '',
    url(r'^api/v1/filemanager', FileManagerApiView.as_view()),
    url(r'^api/v1/file/', include(folder_router.urls)),
    url(r'^api/v1/file/', include(url_file_folder.urls)),
    url(r'^api/v1/file/', include(url_atts_folder.urls)),
    url(r'^api/v1/file/', include(url_images.urls)),
    url(r'^api/v1/file/upload$', FileUploadViewSet.as_view()),
    url(r'^api/v1/file/upload', FileUploadViewSet.as_view()),
    url(r'^page/filecould', FileUploaderTemplate.as_view()),
    url(r'^page/fileManager', FileManagerTemplate.as_view()),

)
