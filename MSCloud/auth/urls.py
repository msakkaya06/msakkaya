from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from auth.views.register_view import RegisterView


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', obtain_auth_token),
]
