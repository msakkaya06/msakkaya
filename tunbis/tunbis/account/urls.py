
from django.urls import path
from . import views


urlpatterns = [
    path('login',views.userLogin,name="user_login"),
    path('register',views.userRegister,name="user_register"),
    path('logout',views.userLogout,name="user_logout"),
    path('profile/<str:username>',views.profileEdit,name='profile'),
    path('password-change',views.password_change,name="password_change"),




]


#PATH SIRALAMAYA GÖRE ÇALIŞIR
# ÖRNEĞİN < > ARASINDAKİ DİNAMİK DEĞERLER ÜSTE TAŞINIRSA DİĞER PATHLERİ EZER