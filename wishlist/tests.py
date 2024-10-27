from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from admin_dashboard.models import RestaurantEntry
from .models import Wishlist
from uuid import uuid4
import json

class WishlistViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.restaurant = RestaurantEntry.objects.create(
            id=uuid4(),
            nama_resto='Test Restaurant',
            rating=4.5,
            alamat='Test Address',
            range_harga=3,
            keramaian_resto=2,  
        )

    def test_show_wishlist(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('wishlist:show_wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist.html')

    def test_add_wishlist(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('wishlist:add_wishlist', args=[self.restaurant.id]), {
            'date_plan': '2023-05-01',
            'additional_note': 'Test note'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue(Wishlist.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_delete_wishlist(self):
        self.client.login(username='testuser', password='12345')
        Wishlist.objects.create(user=self.user, restaurant=self.restaurant)
        response = self.client.post(reverse('wishlist:delete_wishlist', args=[self.restaurant.id]))
        self.assertRedirects(response, reverse('wishlist:show_wishlist'))
        self.assertFalse(Wishlist.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_get_wishlist_content(self):
        self.client.login(username='testuser', password='12345')
        Wishlist.objects.create(user=self.user, restaurant=self.restaurant)
        response = self.client.get(reverse('wishlist:get_wishlist_content'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('content', data)