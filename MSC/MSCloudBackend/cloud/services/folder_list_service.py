from cloud.models import Folder

class FolderListService:
    @staticmethod
    def get_user_folders(user, parent=None):
        return Folder.objects.filter(owner=user, parent=parent).order_by("name")
