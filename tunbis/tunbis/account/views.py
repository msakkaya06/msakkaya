from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import Permission
from tunbisapp.models import TebsGroup, TebsUser
from .forms import LoginUserForm, RegisterUserForm,CustomPasswordChangeForm


# Create your views here.


def userLogin(req):
    if req.user.is_authenticated:
        return redirect("index")
    if req.method == "POST":
        form=LoginUserForm(req,data=req.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(req,username=username,password=password)
            if user is not None:
                login(req,user)
                messages.add_message(req,messages.SUCCESS,"Giriş Başarılı, Hoşgeldiniz " + username)
                nextUrl=req.GET.get("next",None)
                if nextUrl is None:
                    return redirect("index")
                else:
                    return redirect(nextUrl)
            else:
                messages.add_message(req,messages.ERROR,"Kullanıcı Adı ya da Şifre Hatalı")
                return render (req,"account/login.html")
    
    form=LoginUserForm()
    return render (req,"account/login.html",{"form":form})



def password_change(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Kullanıcıyı oturumdan çıkarmamak için
            messages.success(request, 'Parolanız başarıyla değiştirildi.')
            return redirect('profile')  # Profil veya başka bir sayfaya yönlendirin
        else:
            messages.error(request, 'Lütfen formda hata olup olmadığını kontrol edin.')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'account/password_change.html', {'form': form})

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
    

@login_required
def profileEdit(request, username):
    # Giriş yapan kullanıcının sadece kendi profilini düzenlemesi için kontrol
    if request.user.username != username:
        return HttpResponseForbidden("Başka bir kullanıcının profilini düzenleyemezsiniz.")
    
    user = get_object_or_404(TebsUser, username=username)

    groups = user.groups.all()  # Kullanıcının ait olduğu grupları al
    permissions = set()
        # Kullanıcının gruplarından izinleri topla
    for group in groups:
        permissions.update(group.permissions.values_list('codename', flat=True))
    # Kullanıcının gruplarından izinleri topla
      # CustomGroup ile ilişkilendirilen grupları al
    tebs_group = [TebsGroup.objects.get(original_group=group) for group in groups]
    context = {'user': user, 'permissions': permissions,'groups':tebs_group}
    return render(request, "account/profile.html", context)

def userLogout(req):
    logout(req)
    return redirect("index")