import uuid
from django.db import models
from django.contrib.auth.models import User


class ManganJogja(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # tambahkan baris ini
    menu = models.CharField(max_length=255)
    desc = models.TextField()
    nama_resto = models.CharField(max_length=255)
