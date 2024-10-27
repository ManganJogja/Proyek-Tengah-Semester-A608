from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from order_takeaway.models import TakeawayOrder, TakeawayOrderItem
from admin_dashboard.models import RestaurantEntry, MenuEntry
from datetime import time
from decimal import Decimal
import uuid

class OrderTakeawayViewsTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')
        
        # Create a test menu entry
        self.menu_item = MenuEntry.objects.create(
            id=uuid.uuid4(), 
            nama_menu="Test Menu", 
            deskripsi="Delicious test menu item", 
            image_url="http://example.com/image.jpg"
        )

        # Create a test restaurant entry and associate it with the menu
        self.restaurant = RestaurantEntry.objects.create(
            id=uuid.uuid4(), 
            nama_resto="Test Resto", 
            alamat="123 Test St", 
            jenis_kuliner="Test Cuisine", 
            lokasi_resto="Center", 
            range_harga=10000, 
            rating=Decimal("4.5"), 
            suasana="Casual", 
            keramaian_resto=50
        )
        self.menu_item.restaurants.add(self.restaurant)  # Associate the restaurant with the menu item

    def test_create_takeaway_order(self):
        # Test creating a takeaway order with AJAX request
        url = reverse('order_takeaway:create_order_takeaway')
        data = {
            'restaurant': str(self.restaurant.id),  # Ensure UUID is passed as a string
            'order_items': [str(self.menu_item.id)],  # UUID for menu item
            'quantity': 2,
            'pickup_time': time(15, 0).strftime('%H:%M')
        }
        response = self.client.post(
            url,
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Check if the response is successful and order is created
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("success"), True)
        self.assertEqual(TakeawayOrder.objects.count(), 1)
        self.assertEqual(TakeawayOrderItem.objects.count(), 1)
        
    def test_show_takeaway_orders(self):
        # Create a sample order for testing
        order = TakeawayOrder.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            pickup_time=time(15, 0),
            total_price=20000,
            order_time=timezone.now()
        )
        order_item = TakeawayOrderItem.objects.create(
            order=order,
            menu_item=self.menu_item,
            quantity=2,
            price=10000
        )

        # Test if the view returns the order in the context
        url = reverse('order_takeaway:show_order_takeaway')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, order_item.menu_item.nama_menu)
        self.assertContains(response, order.restaurant.nama_resto)

    def test_delete_takeaway_order(self):
        # Create a sample order for testing deletion
        order = TakeawayOrder.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            pickup_time=time(15, 0),
            total_price=20000,
            order_time=timezone.now()
        )

        # Test deleting the order
        url = reverse('order_takeaway:delete_order_takeaway', args=[order.id])
        response = self.client.post(url)
        
        # Check that the order is deleted and redirect is successful
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TakeawayOrder.objects.filter(id=order.id).count(), 0)