from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from reserve.models import ReserveEntry
from admin_dashboard.models import RestaurantEntry
from datetime import date, time

class ReserveEntryViewsTests(TestCase):

    def setUp(self):
        # Set up initial data for tests
        self.client = Client()

        # Create a test user and log them in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Create a test restaurant
        self.restaurant = RestaurantEntry.objects.create()

        # Create a test reservation entry
        self.reserve_entry = ReserveEntry.objects.create(
            user=self.user,
            resto=self.restaurant,
            name='John Doe',
            date=date.today(),
            time=time(12, 0),
            guest_quantity=2,
            email='test@example.com',
            phone=123456789,
            notes='Test note'
        )

    # def test_show_reserve(self):
    #     # Test the show_reserve view
    #     response = self.client.get(reverse('reserve:show_reserve'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'reserve_page.html')
    #     self.assertContains(response, self.reserve_entry.name)

    # def test_create_reserve_entry(self):
    #     # Test the create_reserve_entry view
    #     form_data = {
    #         'name': 'Jane Doe',
    #         'date': '2024-12-01',
    #         'time': '18:00',
    #         'guest_quantity': 4,
    #         'email': 'janedoe@example.com',
    #         'phone': 987654321,
    #         'notes': 'Birthday party'
    #     }

    #     response = self.client.post(reverse('reserve:create_reserve_entry', args=[self.restaurant.id]), form_data)
    #     self.assertEqual(response.status_code, 302)  # Redirect after success
    #     self.assertEqual(ReserveEntry.objects.count(), 2)

    # def test_edit_reserve(self):
    #     # Test the edit_reserve view
    #     form_data = {
    #         'name': 'Updated Name',
    #         'date': '2024-12-01',
    #         'time': '12:30',
    #         'guest_quantity': 3,
    #         'email': 'updated@example.com',
    #         'phone': 123123123,
    #         'notes': 'Updated note'
    #     }

    #     response = self.client.post(reverse('reserve:edit_reserve', args=[self.reserve_entry.id]), form_data)
    #     self.assertEqual(response.status_code, 302)  # Redirect after success
    #     updated_reserve = ReserveEntry.objects.get(pk=self.reserve_entry.id)
    #     self.assertEqual(updated_reserve.name, 'Updated Name')

    # def test_delete_reserve(self):
    #     # Test the delete_reserve view
    #     response = self.client.post(reverse('reserve:delete_reserve', args=[self.reserve_entry.id]))
    #     self.assertEqual(response.status_code, 302)  # Redirect after success
    #     self.assertEqual(ReserveEntry.objects.count(), 0)

    def test_show_json(self):
        # Test the show_json view
        response = self.client.get(reverse('reserve:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_show_json_by_id(self):
        # Test the show_json_by_id view
        response = self.client.get(reverse('reserve:show_json_by_id', args=[self.reserve_entry.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_filter_by_restaurant(self):
        # Test the filter_by_restaurant view with AJAX
        response = self.client.get(reverse('reserve:filter_by_restaurant'), {'restaurant': 'Test Restaurant'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
