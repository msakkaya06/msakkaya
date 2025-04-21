from django.urls import path
from django.urls import path
from . import views


urlpatterns = [
    # Ana klasörler sayfası
    path('', views.folder_list, name='folder_index'),
    
    # Belirli bir klasörün alt klasör ve belgelerini gösteren sayfa
    path('folder/<int:folder_id>/', views.folder_detail, name='folder_detail'),

    # Klasör oluşturma işlemi
    path('create-folder/<int:parent_folder_id>/', views.create_folder, name='create_folder'),

    # Klasör silme işlemi
    path('delete-folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),

    # Belge oluşturma işlemi
    path('create-document/<int:folder_id>/', views.create_document, name='create_document'),

    # Belgeyi düzenleme veya silme işlemi (ekstra, gerekirse eklenebilir)
    path('delete-document/<int:document_id>/', views.delete_document, name='delete_document'),
]
