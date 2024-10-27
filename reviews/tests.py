from django.test import TestCase
from django.contrib.auth.models import User
from admin_dashboard.models import RestaurantEntry
from .models import Review

class ReviewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Log the user in for any login-required views
        self.client.login(username='testuser', password='testpassword')

        self.restaurant = RestaurantEntry.objects.create(
            nama_resto="Test Restaurant",
            alamat="Test Location Address",
            jenis_kuliner="Test Cuisine",
            lokasi_resto="Center",
            range_harga=100,
            rating=4.5,
            suasana="Casual",
            keramaian_resto=50  # atau nilai integer sesuai kebutuhan
        )

    def test_add_review(self):
        # Add test logic here for adding a review
        response = self.client.post(f'/reviews/add_review/{self.restaurant.id}/', {
            'rating': 4,
            'comment': 'Great place!'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect after successful review submission

    def test_delete_review(self):
    # Buat instance review untuk menguji penghapusan
        review = Review.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            rating=4,
            comment='Nice experience'
        )
        response = self.client.post(f'/reviews/delete_review/{review.id}/')
        self.assertEqual(response.status_code, 302)  # Cek untuk redirect setelah penghapusan berhasil

    def test_review_card_view(self):
        response = self.client.get(f'/reviews/card/{self.restaurant.id}/')
        self.assertEqual(response.status_code, 200)  # Check if the view loads correctly
