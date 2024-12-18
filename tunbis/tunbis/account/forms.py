from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.forms import widgets
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password, check_password

class LoginUserForm(AuthenticationForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields["username"].widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"Sicil"})
        self.fields["password"].widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"Şifre","type":"Password"})

class RegisterUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=("username","email")

    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields["username"].widget=widgets.TextInput(attrs={"class":"form-control"})
        self.fields["password1"].widget=widgets.PasswordInput(attrs={"class":"form-control"})
        self.fields["password2"].widget=widgets.PasswordInput(attrs={"class":"form-control"})
        self.fields["email"].widget=widgets.EmailInput(attrs={"class":"form-control"})

    def clean_email(self):
        email=self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            self.add_error("email","Girdiğiniz E-Posta Adresi Sistemde Mevcut")
           
        return email


class CustomPasswordChangeForm(PasswordChangeForm):
    security_question = forms.CharField(
        label="Güvenlik Sorusu",
        max_length=100,
        required=False,
        help_text="Kendi belirlediğiniz güvenlik sorusu."
    )
    security_answer = forms.CharField(
        label="Güvenlik Cevabı",
        widget=forms.PasswordInput,
        required=False,
        help_text="Bu güvenlik sorusuna vereceğiniz cevap."
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        # Formda güvenlik sorusu ve cevabı varsa kullanıcıya kaydedin
        user.security_question = self.cleaned_data.get('security_question')
        user.security_answer = make_password(self.cleaned_data.get('security_answer'))
        if commit:
            user.save()
        return user

