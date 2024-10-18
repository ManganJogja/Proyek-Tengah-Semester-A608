from django import forms
from reserve.models import ReserveEntry
from datetime import date

class ReserveEntryForm(forms.ModelForm):
    class Meta:
        model = ReserveEntry
        fields = ["name", "date", "time", "guest_quantity", "email", "phone", "notes"]
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'min': date.today().strftime('%Y-%m-%d'),  # Membatasi tanggal minimum menjadi hari ini
                    'class': 'form-control'
                }),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
      
