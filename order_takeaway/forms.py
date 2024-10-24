from django import forms
from order_takeaway.models import TakeawayOrder
from django.core.validators import MinValueValidator

class TakeawayOrderForm(forms.ModelForm):
    quantity = forms.IntegerField(
        validators=[MinValueValidator(1)],  
        widget=forms.NumberInput(attrs={
            'min': 1,
            'class': 'form-control'
        })
    )

    class Meta:
        model = TakeawayOrder
        fields = ["menu_item", "quantity", "pickup_time"]
        
        widgets = {
            'pickup_time': forms.TimeInput(
                attrs={
                    'type': 'time', 
                    'class': 'form-control'
                }
            )
        }
