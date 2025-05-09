from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from accounts.views.make_admin_view import MakeAdminView
from accounts.views.protected_admin_view import AdminOnlyView
from accounts.views.change_password_view import ChangePasswordView

from .views.login_view import LoginView
from .views.logout_view import LogoutView
from .views.me_view import MeView
from .views.register_view import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # login
    TokenRefreshView,     # token yenile
    TokenVerifyView       # token geçerli mi
)



urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('me/', MeView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("admin-area/", AdminOnlyView.as_view(), name="admin_area"),
    path("make-admin/", MakeAdminView.as_view(), name="make_admin"),
    
]
