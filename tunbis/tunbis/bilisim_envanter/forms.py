from django import forms
from tunbisapp.models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['device_type', 'brand', 'model', 'serial_number', 'quantity']
        labels = {
            'device_type': 'Cihaz Türü',
            'brand': 'Marka',
            'model': 'Model',
            'serial_number': 'Seri Numarası',
            'quantity': 'Adet',
        }
        widgets = {
            'device_type': forms.Select(attrs={'class': 'form-control mb-2'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
