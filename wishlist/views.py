from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from admin_dashboard.models import RestaurantEntry
from .models import Wishlist
from .forms import WishlistForm

@login_required
def show_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('restaurant')
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'wishlist.html', context)


@login_required
def add_wishlist(request, restaurant_id):
    restaurant = get_object_or_404(RestaurantEntry, id=restaurant_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, restaurant=restaurant)

    if request.method == 'POST':
        form = WishlistForm(request.POST, instance=wishlist_item)
        if form.is_valid():
            form.save()
            return redirect('show_wishlist')
    else:
        form = WishlistForm(instance=wishlist_item)

    context = {
        'restaurant': restaurant,
        'form': form,
    }
    return render(request, 'add_wishlist_plan.html', context)

@login_required
def delete_wishlist(request, restaurant_id):
    wishlist_item = get_object_or_404(Wishlist, user=request.user, restaurant_id=restaurant_id)
    wishlist_item.delete()
    return redirect('show_wishlist')