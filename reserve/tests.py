from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from reserve.models import ReserveEntry
from admin_dashboard.models import RestaurantEntry
from reserve.forms import ReserveEntryForm
from django.utils import timezone

User = get_user_model()

class ReserveViewTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        # Create a restaurant
        self.restaurant = RestaurantEntry.objects.create(
            nama_resto='Test Restaurant',
            alamat='123 Test St',
            jenis_kuliner='Italian',
            lokasi_resto='Downtown',
            range_harga=200,
            rating=4.5,
            suasana='Cozy',
            keramaian_resto=30
        )

    def test_show_reserve(self):
        # Create a reservation for the user
        ReserveEntry.objects.create(
            user=self.user,
            resto=self.restaurant,
            name='John Doe',
            date=timezone.now().date(),
            time=timezone.now().time(),
            guest_quantity=2,
            email='john@example.com',
            phone=1234567890,
            notes='No special requests'
        )

        # Make a GET request to the show_reserve view
        response = self.client.get(reverse('reserve:show_reserve'))

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Restaurant')  # Check if the restaurant is listed
        self.assertContains(response, 'John Doe')  # Check if the reservation is listed

    def test_create_reserve_entry(self):
        # Make a POST request to create a reservation
        response = self.client.post(reverse('reserve:create_reserve_entry', args=[self.restaurant.id]), {
            'name': 'Jane Doe',
            'date': timezone.now().date(),
            'time': timezone.now().time(),
            'guest_quantity': 4,
            'email': 'jane@example.com',
            'phone': 9876543210,
            'notes': 'Window seat please'
        })

        # Check that a new reservation was created
        self.assertEqual(ReserveEntry.objects.count(), 1)
        self.assertEqual(response.status_code, 302)  # Check for redirect



    def test_delete_reserve_entry(self):
        # Create a reservation to delete
        reserve_entry = ReserveEntry.objects.create(
            user=self.user,
            resto=self.restaurant,
            name='John Doe',
            date=timezone.now().date(),
            time=timezone.now().time(),
            guest_quantity=2,
            email='john@example.com',
            phone=1234567890,
            notes='No special requests'
        )

        # Delete the reservation
        response = self.client.post(reverse('reserve:delete_reserve', args=[reserve_entry.id]))

        # Check that the reservation was deleted
        self.assertEqual(ReserveEntry.objects.count(), 0)
        self.assertEqual(response.status_code, 302)  # Check for redirect

    def test_show_json(self):
        # Create a reservation
        reserve_entry = ReserveEntry.objects.create(
            user=self.user,
            resto=self.restaurant,
            name='John Doe',
            date=timezone.now().date(),
            time=timezone.now().time(),
            guest_quantity=2,
            email='john@example.com',
            phone=1234567890,
            notes='No special requests'
        )

        # Make a GET request to show_json
        response = self.client.get(reverse('reserve:show_json'))

        # Check that the response contains the reservation data
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"name": "John Doe"')


    def test_show_reserve_url(self):
        response = self.client.get(reverse('reserve:show_reserve'))
        self.assertEqual(response.status_code, 200)  # Check for successful access

    def test_create_reserve_entry_url(self):
        response = self.client.get(reverse('reserve:create_reserve_entry', args=[self.restaurant.pk]))
        self.assertEqual(response.status_code, 200)  # Check for successful access

    
    def test_delete_reserve_url(self):
        reserve_entry = ReserveEntry.objects.create(
            user=self.user,
            resto=self.restaurant,
            name='John Doe',
            date='2024-10-30',
            time='18:00',
            guest_quantity=2,
            email='john@example.com',
            phone=1234567890,
            notes='None'
        )
        response = self.client.post(reverse('reserve:delete_reserve', args=[reserve_entry.id]))
        self.assertEqual(response.status_code, 302)  # Check for redirect after deletion
        self.assertFalse(ReserveEntry.objects.filter(id=reserve_entry.id).exists())  # Ensure it's deleted

    def test_show_json_url(self):
        response = self.client.get(reverse('reserve:show_json'))
        self.assertEqual(response.status_code, 200)  # Check for successful access

    def test_show_json_by_id_url(self):
        reserve_entry = ReserveEntry.objects.create(
            user=self.user,
            resto=self.restaurant,
            name='John Doe',
            date='2024-10-30',
            time='18:00',
            guest_quantity=2,
            email='john@example.com',
            phone=1234567890,
            notes='None'
        )
        response = self.client.get(reverse('reserve:show_json_by_id', args=[reserve_entry.id]))
        self.assertEqual(response.status_code, 200)  # Check for successful access
