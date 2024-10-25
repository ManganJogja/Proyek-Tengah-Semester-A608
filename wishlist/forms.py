from django import forms
from .models import Wishlist

class WishlistForm(forms.ModelForm):
       class Meta:
           model = Wishlist
           fields = ['date_plan', 'additional_note']
           widgets = {
               'date_plan': forms.DateInput(attrs={'type': 'date'}),
               'additional_note': forms.Textarea(attrs={'rows': 3}),
           }
