from cloud.models import File

class FileListService:
    @staticmethod
    def get_user_files(user, folder=None):
        return File.objects.filter(owner=user, folder=folder).order_by("-uploaded_at")
