from django.db import models
from django.contrib.auth.models import User
from admin_dashboard.models import RestaurantEntry, MenuEntry
import uuid

class TakeawayOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(RestaurantEntry, on_delete=models.CASCADE)
    order_items = models.ManyToManyField(MenuEntry, through='TakeawayOrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_prep_time = models.DurationField()
    order_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} at {self.restaurant.nama_resto}"
    
class TakeawayOrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(TakeawayOrder, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuEntry, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.nama_menu} for order {self.order.id}"