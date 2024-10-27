from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import MenuEntry, RestaurantEntry

class AdminDashboardTest(TestCase):
    def setUp(self):
        # Buat user admin
        self.client = Client()
        self.staff_user = User.objects.create_user(username='adminuser', password='adminpassword')
        self.staff_user.is_staff = True
        self.staff_user.save()

        MenuEntry.objects.create(
            nama_menu="Menu 1",
            deskripsi="Deskripsi 1",
            image_url="https://tse3.mm.bing.net/th?id=OIP.arYo3DDmggc9WiXWlxHsWAHaEK&pid=Api&P=0&h=180"
            )

        self.restaurant = RestaurantEntry.objects.create(
            nama_resto='Restoran 1',
            alamat='Alamat 1',
            jenis_kuliner='Indonesia',
            lokasi_resto='2 km',
            range_harga='10000',
            rating='5',
            suasana='Santai',
            keramaian_resto='5'
        )

    def test_admin_access(self):
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.get(reverse('admin_dashboard:admin_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_dashboard.html')

    def test_menus_page_access(self):
            self.client.login(username='adminuser', password='adminpassword')
            response = self.client.get(reverse('admin_dashboard:all_menus_admin'))

            self.assertEqual(response.status_code, 200)
    
    def test_create_menu_page_access(self):
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.get(reverse('admin_dashboard:create_menu_entry'))  # Ganti dengan URL yang sesuai
        self.assertEqual(response.status_code, 200)
    
    def test_create_menu(self):
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.post(reverse('admin_dashboard:create_menu_entry'), {
            'nama_menu': 'Menu 3',
            'deskripsi': 'Deskripsi 3',
            'image_url': 'https://example.com/image3.jpg'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(MenuEntry.objects.filter(nama_menu='Menu 3').exists())  
    
    def test_update_menu(self):
        menu = MenuEntry.objects.create(nama_menu='Menu 4', deskripsi='Deskripsi 4', image_url='https://example.com/image4.jpg')
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.post(reverse('admin_dashboard:edit_menu', args=[menu.pk]), {
            'nama_menu': 'Updated Menu 4',
            'deskripsi': 'Updated Deskripsi 4',
            'image_url': 'https://example.com/image4_updated.jpg'
        })
        self.assertEqual(response.status_code, 302) 
        menu.refresh_from_db()  
        self.assertEqual(menu.nama_menu, 'Updated Menu 4')

    def test_delete_menu(self):
        menu = MenuEntry.objects.create(nama_menu='Menu 5', deskripsi='Deskripsi 5', image_url='https://example.com/image5.jpg')
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.post(reverse('admin_dashboard:delete_menu', args=[menu.pk])) 
        self.assertEqual(response.status_code, 302)  
        self.assertFalse(MenuEntry.objects.filter(pk=menu.pk).exists())  

    def test_create_restaurant(self):
        menu = MenuEntry.objects.create(nama_menu='Menu Test', deskripsi='Deskripsi Menu Test', image_url='https://example.com/image_test.jpg')
        response = self.client.post(reverse('admin_dashboard:create_resto_entry', args=[menu.pk]), {
            'nama_resto': 'Restoran Test',
            'alamat': 'Alamat Test',
            'jenis_kuliner': 'Indonesian',
            'lokasi_resto': '1 km',
            'range_harga': '5000',
            'rating': '4',
            'suasana': 'Santai',
            'keramaian_resto': '3'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(RestaurantEntry.objects.filter(nama_resto='Restoran Test').exists())
        restaurant = RestaurantEntry.objects.get(nama_resto='Restoran Test')
        self.assertIn(menu, restaurant.menus.all())

    def test_edit_restaurant(self):
        menu = MenuEntry.objects.create(nama_menu='Menu 1', deskripsi='Deskripsi 1', image_url='https://example.com/image1.jpg')
        self.restaurant = RestaurantEntry.objects.create(
            nama_resto='Restoran 1',
            alamat='Alamat 1',
            jenis_kuliner='Indonesia',
            lokasi_resto='1 km',
            range_harga='10000',
            rating='5',
            suasana='Santai',
            keramaian_resto='5'
        )
        self.restaurant.menus.add(menu)

        self.client.login(username='adminuser', password='adminpassword')

        response = self.client.post(reverse('admin_dashboard:edit_resto', args=[self.restaurant.pk]), {
            'nama_resto': 'Restoran 1 Edit',
            'alamat': 'Alamat 1',
            'jenis_kuliner': 'Indonesia',
            'lokasi_resto': '2 km',
            'range_harga': 10000,
            'rating': 5,
            'suasana': 'Santai',
            'keramaian_resto': 5
        })
        self.assertEqual(response.status_code, 302)
        
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.nama_resto, 'Restoran 1 Edit')
        self.assertEqual(self.restaurant.alamat, 'Alamat 1')
        self.assertEqual(self.restaurant.jenis_kuliner, 'Indonesia')
        self.assertEqual(self.restaurant.lokasi_resto, '2 km')
        self.assertEqual(self.restaurant.range_harga, 10000)
        self.assertEqual(self.restaurant.rating, 5)
        self.assertEqual(self.restaurant.suasana, 'Santai')
        self.assertEqual(self.restaurant.keramaian_resto, 5)

    def test_delete_restaurant(self):
        menu = MenuEntry.objects.create(nama_menu='Menu 1', deskripsi='Deskripsi 1', image_url='https://example.com/image1.jpg')
        self.restaurant = RestaurantEntry.objects.create(
            nama_resto='Restoran 1',
            alamat='Alamat 1',
            jenis_kuliner='Indonesia',
            lokasi_resto='1 km',
            range_harga='10000',
            rating='5',
            suasana='Santai',
            keramaian_resto='5'
        )
        self.restaurant.menus.add(menu)

        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.post(reverse('admin_dashboard:delete_resto', args=[self.restaurant.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(RestaurantEntry.objects.filter(pk=self.restaurant.pk).exists())
