from django import forms
from reserve.models import ReserveEntry
from datetime import date
from django.core.validators import MinValueValidator

class ReserveEntryForm(forms.ModelForm):
    guest_quantity = forms.IntegerField(
        validators=[MinValueValidator(1)],  # Validator for minimum value 1
        widget=forms.NumberInput(attrs={
            'min': 1,  # HTML 'min' attribute to prevent numbers less than 1
            'class': 'form-control',
            'placeholder': 'enter your Guest Quantity'
            
        })
    )
    class Meta:
        model = ReserveEntry
        fields = ["name", "date", "time", "email", "phone", "guest_quantity", "notes"]
        widgets = {
            "name": forms.TextInput(attrs={'placeholder': 'enter your Full Name'}),
            'date': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'min': date.today().strftime('%Y-%m-%d'),  # Membatasi tanggal minimum menjadi hari ini
                    'class': 'form-control'
                }),
            'time': forms.TimeInput(
                attrs={
                    'type': 'time', 
                    'class': 'form-control', 
                    'placeholder': 'Enter time in HH:MM format'
                },
                format='%H:%M'  # Format waktu sebagai HH:MM
            ),            
            "email": forms.EmailInput(attrs={'placeholder': 'enter your Email Address'}),
            "phone": forms.NumberInput(attrs={'placeholder': 'enter your Phone Number'}),
            "notes": forms.TextInput(attrs={'placeholder': 'enter your Additional Notes'}),       
        }
      
