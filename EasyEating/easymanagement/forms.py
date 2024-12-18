from django import forms
from django.forms import BooleanField, FileInput, HiddenInput, TextInput,Textarea

from .models import Desk, Produce


class DeskCreateForm(forms.ModelForm):
    class Meta:
        model = Desk
        fields = ('name','business',)
        labels={
            'name':'Masa Adı',
        }
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'type':"Input"}),
            'business':HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['business'].initial = user.business


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Produce
        fields = ('name', 'description', 'price', 'image','id')
        labels = {
            'name': 'Ürün Adı',
            'description': 'Ürün Açıklama',
            'price': 'Fiyat',
            'image': 'Fotoğraf'   }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'id':HiddenInput(),
        }
