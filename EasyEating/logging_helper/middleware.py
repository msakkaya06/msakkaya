from django.utils.timezone import timezone
from .log_base import UserActivityLog

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else None
        if user:
            action = f"Visited {request.path}"
            activity_log = UserActivityLog(user=user.username, action=action)
            activity_log.send()  # Log gönder

        response = self.get_response(request)
        return response
