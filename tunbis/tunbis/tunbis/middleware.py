from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect

class Custom405Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if isinstance(response, HttpResponseForbidden):
            # Eğer 405 hatası alınırsa, kullanıcıyı belirlediğiniz sayfaya yönlendir
            return HttpResponseRedirect(reverse('index'))  # index yerine yönlendirmek istediğiniz sayfanın adını verin
        return response


from django.http import HttpResponseForbidden

class PersonelPermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/personel/') and not request.user.groups.filter(name='personel').exists():
            return HttpResponseForbidden()
        return self.get_response(request)
