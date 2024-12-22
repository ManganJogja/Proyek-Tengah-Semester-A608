from django import forms
from order_takeaway.models import TakeawayOrder, TakeawayOrderItem
from admin_dashboard.models import RestaurantEntry, MenuEntry
from django.core.validators import MinValueValidator

class TakeawayOrderForm(forms.ModelForm):
    restaurant = forms.ModelChoiceField(
        queryset=RestaurantEntry.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'min': 1, 'class': 'form-control'})
    )

    class Meta:
        model = TakeawayOrder
        fields = ['restaurant', 'order_items', 'quantity', 'pickup_time']
        widgets = {
            'pickup_time': forms.TimeInput(attrs={'type': 'time', 
            'class': 'form-control',
            'placeholder': 'Enter time in HH:MM format'
                },
                format='%H:%M'  # Format waktu sebagai HH:MM
            ),     
        }