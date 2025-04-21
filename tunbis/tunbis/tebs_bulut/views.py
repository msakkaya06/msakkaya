from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import DocumentType, Folder, Document


def folder_list(request):
    folders = Folder.objects.filter(user=request.user, parent=None)
    return render(request, 'tebs_bulut/index.html', {'folders': folders})

def folder_detail(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    subfolders = Folder.objects.filter(user=request.user, parent=folder)
    documents = Document.objects.filter(folder=folder)
    return render(request, 'tebs_bulut/folder_detail.html', {
        'folder': folder,
        'subfolders': subfolders,
        'documents': documents
    })

def create_folder(request, parent_folder_id):
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        parent_folder = Folder.objects.get(id=parent_folder_id, user=request.user)
        new_folder = Folder.objects.create(
            name=folder_name,
            user=request.user,
            parent=parent_folder
        )
        return JsonResponse({'status': 'success', 'folder_id': new_folder.id})

def delete_folder(request, folder_id):
    folder = Folder.objects.get(id=folder_id, user=request.user)
    folder.delete()
    return JsonResponse({'status': 'success'})

def create_document(request, folder_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        doc_type = request.POST.get('doc_type')
        doc_type_enum = DocumentType[doc_type.upper()]
        folder = Folder.objects.get(id=folder_id, user=request.user)
        document = Document.objects.create(
            title=title,
            user=request.user,
            folder=folder,
            document_type=doc_type_enum
        )
        return JsonResponse({'status': 'success', 'document_id': document.id})

def delete_document(request, document_id):
    document = Document.objects.get(id=document_id, user=request.user)
    document.delete()
    return JsonResponse({'status': 'success'})
