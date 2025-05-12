from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from accounts.views.admin_user_list_view import AdminUserListView
from accounts.views.custom_jwt_login_view import CustomTokenObtainPairView
from accounts.views.make_admin_view import MakeAdminView
from accounts.views.protected_admin_view import AdminOnlyView
from accounts.views.change_password_view import ChangePasswordView
from accounts.views.remove_admin_view import RemoveAdminView
from accounts.views.toggle_active_view import ToggleActiveView
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
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("admin-area/", AdminOnlyView.as_view(), name="admin_area"),
    path("make-admin/", MakeAdminView.as_view(), name="make_admin"),
    path("admin/users/", AdminUserListView.as_view(), name="admin_user_list"),
    path("remove-admin/", RemoveAdminView.as_view(), name="remove_admin"),
    path("toggle-active/", ToggleActiveView.as_view(), name="toggle_active"),
]
