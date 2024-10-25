from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from admin_dashboard.models import RestaurantEntry
from .models import Wishlist
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import logging
from django.template.loader import render_to_string
from .forms import WishlistForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from uuid import UUID

logger = logging.getLogger(__name__)



@login_required
def show_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('restaurant')
    context = {
        'last_login': request.COOKIES.get('last_login', 'No recent login'),
        'wishlist_items': wishlist_items,
    }
    return render(request, 'wishlist.html', context)


@login_required
def add_wishlist(request, restaurant_id: UUID):
    restaurant = get_object_or_404(RestaurantEntry, id=restaurant_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, restaurant=restaurant)

    if request.method == 'POST':
        form = WishlistForm(request.POST, instance=wishlist_item)
        if form.is_valid():
            form.save()
            return redirect('wishlist:show_wishlist')
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


@login_required
@require_POST
def toggle_wishlist(request, restaurant_id):
    restaurant = get_object_or_404(RestaurantEntry, id=restaurant_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        restaurant=restaurant,
        defaults={'date_plan': None}
    )
    
    if not created:
        wishlist_item.delete()
        return JsonResponse({'added': False})
    
    return JsonResponse({'added': True})

@login_required
def get_wishlist_content(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('restaurant')
    context = {
        'wishlist_items': wishlist_items,
    }
    content = render_to_string('wishlist_content.html', context, request=request)
    return JsonResponse({'content': content})

@login_required
def delete_wishlist(request, restaurant_id):
    # Get wishlist item berdasarkan restaurant_id
    wishlist_item = get_object_or_404(Wishlist, user=request.user, restaurant_id=restaurant_id)
    # Hapus wishlist item
    wishlist_item.delete()
    # Kembali ke halaman wishlist
    return HttpResponseRedirect(reverse('wishlist:show_wishlist'))
