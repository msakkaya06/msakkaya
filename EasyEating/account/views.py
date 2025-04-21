from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from easymanagement.models import EEUser  # Kullanıcı modelinizin doğru adı

from order.views.web_views import desk_is_logout
from .forms import LoginUserForm, RegisterUserForm


# Create your views here.


def userLogin(req):
    if req.user.is_authenticated:
        if req.user.is_manager:
            return HttpResponseRedirect("/management/dashboard")  # Yönetici ise Dashboard sayfasına yönlednir
        else:
            return HttpResponseRedirect("/order")  # Yönetici değilse masadır. Sipariş sayfasına yönlendir
    if req.method == "POST":
        form = LoginUserForm(req, data=req.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(req, username=username, password=password)
            if user is not None:
                login(req, user)
                messages.success(req, "Giriş Başarılı, Hoşgeldiniz " + username)
                return HttpResponseRedirect("/order/")  # Giriş yapıldıktan sonra /order/ sayfasına yönlendir
            else:
                # Kullanıcı adı veya şifre hatalı
                messages.error(req, "Kullanıcı adı veya şifre hatalı.")
                return render(req, "account/login.html", {"form": form})  # Hata durumunda login formunu tekrar göster
    else:
        form = LoginUserForm()
    return render(req, "account/login.html", {"form": form})





def desk_login(request):
    if request.method == "GET":
        username = request.GET.get("username")
        token = request.GET.get("token")
        print(username)
        print(token)
        if username and token:
            try:
                # Kullanıcıyı bul
                user = EEUser.objects.get(username=username)
                print(user.token)
                if user:
                    login(request, user)
                    return redirect("/order/")  # Sipariş sayfasına yönlendir
            except EEUser.DoesNotExist:
                messages.error(request, "Geçersiz karekod veya kullanıcı.")
        else:
            messages.error(request, "Kullanıcı adı veya token eksik.")

    return HttpResponseRedirect("/account/login")  # Doğru sayfaya yönlendir




def userRegister(req):
    if req.method == "POST":
        form=RegisterUserForm(req.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password1")
            user=authenticate(req,username=username,password=password)
            login(req,user)
            return redirect("index")
        else:
            return render(req,"account/register.html",{"form":form})
    else:
        form=RegisterUserForm()
        return render (req,"account/register.html",{"form":form})
    
def profileEdit(req):
    return render (req,"account/profile.html")
    

def userLogout(req):
    if req.user.is_desk==True:
        desk_is_logout(req)
    logout(req)
    return redirect("index")



    