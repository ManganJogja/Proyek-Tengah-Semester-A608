from django import forms
from reserve.models import ReserveEntry
from datetime import date
from django.core.validators import MinValueValidator

class ReserveEntryForm(forms.ModelForm):
    guest_quantity = forms.IntegerField(
        validators=[MinValueValidator(1)],  # Validator for minimum value 1
        widget=forms.NumberInput(attrs={
            'min': 1,  # HTML 'min' attribute to prevent numbers less than 1
            'class': 'form-control'
        })
    )
    class Meta:
        model = ReserveEntry
        fields = ["name", "date", "time", "email", "phone", "guest_quantity", "notes"]
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'min': date.today().strftime('%Y-%m-%d'),  # Membatasi tanggal minimum menjadi hari ini
                    'class': 'form-control'
                }),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            
        }
      
