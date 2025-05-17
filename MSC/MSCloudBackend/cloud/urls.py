from django.urls import path

from cloud.views.file_list_views import FileListAPIView
from cloud.views.file_views import FileUploadAPIView
from cloud.views.folder_detail_views import FolderDetailAPIView
from cloud.views.folder_list_views import FolderListAPIView
from cloud.views.folder_views import CreateFolderAPIView

urlpatterns = [
    path("folders/create/", CreateFolderAPIView.as_view(), name="create-folder"),
    path("files/upload/", FileUploadAPIView.as_view(), name="file-upload"),
    path("folders/", FolderListAPIView.as_view(), name="list-folders"),
    path("files/", FileListAPIView.as_view(), name="list-files"),
    path("folders/<int:pk>/", FolderDetailAPIView.as_view(), name="folder-detail"),
]
