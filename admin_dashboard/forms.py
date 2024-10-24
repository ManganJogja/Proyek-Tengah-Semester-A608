from django import forms
from .models import MenuEntry, RestaurantEntry

class MenuEntryForm(forms.ModelForm):
    class Meta:
        model = MenuEntry
        fields = ['nama_menu', 'deskripsi', 'image_url']

class RestaurantEntryForm(forms.ModelForm):
    class Meta:
        model = RestaurantEntry
        fields = ['nama_resto', 'alamat', 'jenis_kuliner', 'lokasi_resto', 'range_harga', 'rating', 'suasana', 'keramaian_resto']
