import json
from admin_dashboard.models import RestaurantEntry, MenuEntry  # Import your models

def load_seed_data():
    # Load JSON data
    with open('main/MenuDatabase.json', 'r') as f:
        data = json.load(f)

    default_image_url = "https://tribratanews.polri.go.id/web/image/blog.post/50469/image"
    # Dictionary to hold the already created menu entries
    menu_cache = {}

    # Iterate over each item in the JSON data
    for item in data:
        # Check if the menu already exists, otherwise create it
        if item['nama_menu'] not in menu_cache:
            menu_entry = MenuEntry.objects.create(
                id=item['pk'],
                nama_menu=item['nama_menu'],
                deskripsi=item['deskripsi'],
                image_url=default_image_url,
            )
            menu_cache[item['nama_menu']] = menu_entry
        else:
            menu_entry = menu_cache[item['nama_menu']]

        # Check if a restaurant with the same name already exists or create it
        resto, created = RestaurantEntry.objects.get_or_create(
            nama_resto=item['nama_resto'],
            defaults={
                'alamat': item['alamat'],
                'jenis_kuliner': item['jenis_kuliner'],
                'lokasi_resto': item['lokasi_resto'],
                'range_harga': item['range_harga'] or 0,
                'rating': item['rating'] or 0.0,
                'suasana': item['suasana'],
                'keramaian_resto': item['keramaian_resto'] or 1,
            }
        )

        # Associate the restaurant with the menu item
        menu_entry.restaurants.add(resto)

    # Save the associations
    for menu in menu_cache.values():
        menu.save()

if __name__ == "__main__":
    load_seed_data()
