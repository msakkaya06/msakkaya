"""
URL configuration for tunbis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('tunbisapp.urls'),name="tebs_index"),
    path('account/',include('account.urls')),
    path('personel/',include('personel.urls')),
    path('idari-buro/',include('idariburo.urls')),
    path('bilisim-envanter/',include('bilisim_envanter.urls')),
    path('bilisim-ariza-takip/',include('ariza_takip.urls')),
    path('api/',include('api.urls')),
    path('tebs-bulut/',include('tebs_bulut.urls')),






] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
