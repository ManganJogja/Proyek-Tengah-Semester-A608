import uuid
from django.db import models

from django.contrib.auth.models import User

class RestaurantEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_resto = models.CharField(max_length=255)
    lokasi = models.CharField(max_length=255)
    range_harga = models.CharField(max_length=50)
    jenis_kuliner = models.CharField(max_length=50)

class MenuEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_menu = models.CharField(max_length=100)
    deskripsi = models.TextField()
    image_url = models.URLField(max_length=200)
    restaurants = models.ManyToManyField(RestaurantEntry, related_name='menus')

