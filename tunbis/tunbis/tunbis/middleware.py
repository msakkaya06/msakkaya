from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect
from django.http import HttpResponseForbidden

class Custom405Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if isinstance(response, HttpResponseForbidden):
            # Eğer 405 hatası alınırsa, kullanıcıyı belirlediğiniz sayfaya yönlendir
            return HttpResponseRedirect(reverse('index'))  # index yerine yönlendirmek istediğiniz sayfanın adını verin
        return response
    
    
GROUP_URL_MAP = {
    'personel': '/personel/',
    'bilisim_envanter': '/bilisim-envanter/',
    'idari_buro': '/idari-buro/',
}

class RoleBasedPermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        for group, path_prefix in GROUP_URL_MAP.items():
            if request.path.startswith(path_prefix) and not request.user.groups.filter(name=group).exists():
                return HttpResponseForbidden()
        return self.get_response(request)
