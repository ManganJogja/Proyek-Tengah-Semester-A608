from django.shortcuts import render
from admin_dashboard.models import RestaurantEntry

def show_wishlist(request):
    restaurants = RestaurantEntry.objects.all()
    context = {
        'name': 'hanifa',
        'restaurants': restaurants,
    }
    return render(request, 'wishlist.html', context)

# Create your views here.
