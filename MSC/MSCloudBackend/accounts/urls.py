from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views.login_view import LoginView
from .views.logout_view import LogoutView
from .views.me_view import MeView
from .views.register_view import RegisterView



urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('me/', MeView.as_view()),
    
]
