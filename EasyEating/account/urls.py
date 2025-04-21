
from django.urls import path
from . import views


urlpatterns = [
    path('login',views.userLogin,name="user_login"),
    path('desk-login',views.desk_login,name="desk_login"),
    path('register',views.userRegister,name="user_register"),
    path('logout',views.userLogout,name="user_logout"),
    path('profile/<str:username>',views.profileEdit,name='profile'),



]


#PATH SIRALAMAYA GÖRE ÇALIŞIR
# ÖRNEĞİN < > ARASINDAKİ DİNAMİK DEĞERLER ÜSTE TAŞINIRSA DİĞER PATHLERİ EZER