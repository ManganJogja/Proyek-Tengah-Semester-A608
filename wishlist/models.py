from django.db import models
from django.contrib.auth.models import User
from admin_dashboard.models import RestaurantEntry
from django.utils import timezone

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(RestaurantEntry, on_delete=models.CASCADE, related_name='wishlists')
    date_plan = models.DateField(null=True, blank=True)  # Ubah ini menjadi nullable
    additional_note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s wishlist for {self.restaurant.name}"

    class Meta:
        unique_together = ['user', 'restaurant']