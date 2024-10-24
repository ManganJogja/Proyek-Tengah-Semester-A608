import uuid
from django.db import models
from decimal import Decimal

from django.contrib.auth.models import User

class RestaurantEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_resto = models.CharField(max_length=255)
    alamat = models.TextField()
    jenis_kuliner = models.CharField(max_length=50)
    lokasi_resto = models.CharField(max_length=10)
    range_harga = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    suasana = models.CharField(max_length=255)
    keramaian_resto = models.IntegerField()

class MenuEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    no = models.IntegerField()
    nama_menu = models.CharField(max_length=100)
    deskripsi = models.TextField()
    image_url = models.URLField(max_length=200)
    restaurants = models.ManyToManyField(RestaurantEntry, related_name='menus')

