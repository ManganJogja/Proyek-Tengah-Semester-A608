from django import forms
from .models import MenuEntry, RestaurantEntry

class MenuForm(forms.ModelForm):
    class Meta:
        model = MenuEntry
        fields = ['nama_menu', 'deskripsi', 'image_url']

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = RestaurantEntry
        fields = ['nama_resto', 'lokasi', 'range_harga', 'jenis_kuliner']
