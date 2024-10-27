from django.db import models
from django.contrib.auth.models import User
from admin_dashboard.models import RestaurantEntry  # Mengimpor RestaurantEntry dari admin_dashboard

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(RestaurantEntry, on_delete=models.CASCADE)  # Menggunakan RestaurantEntry
    name = models.CharField(max_length=100, blank=True, null=True)  # Optional reviewer name
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username}"
