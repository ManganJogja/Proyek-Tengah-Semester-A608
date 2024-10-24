import uuid
from django.db import models
from main.models import User


class ReserveEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField()    
    time = models.TimeField()
    guest_quantity = models.IntegerField(default=1)
    email = models.EmailField()
    phone = models.IntegerField()
    notes = models.TextField(max_length=255, blank=True)
    