from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.forms import widgets

from easymanagement.models import EEUser

class LoginUserForm(AuthenticationForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields["username"].widget=widgets.TextInput(attrs={"class":"form-control"})
        self.fields["password"].widget=widgets.TextInput(attrs={"class":"form-control"})

class RegisterUserForm(UserCreationForm):
    class Meta:
        model=EEUser
        fields=("username","email","is_manager",)

    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields["username"].widget=widgets.TextInput(attrs={"class":"form-control"})
        self.fields["password1"].widget=widgets.PasswordInput(attrs={"class":"form-control"})
        self.fields["password2"].widget=widgets.PasswordInput(attrs={"class":"form-control"})
        self.fields["email"].widget=widgets.EmailInput(attrs={"class":"form-control"})
    
     
     



    def clean_email(self):
        email=self.cleaned_data.get("email")

        if EEUser.objects.filter(email=email).exists():
            self.add_error("email","Girdiğiniz E-Posta Adresi Sistemde Mevcut")
           
        return email

