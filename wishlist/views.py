from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from admin_dashboard.models import RestaurantEntry
from .models import Wishlist
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
import logging
from .forms import WishlistForm
from django.urls import reverse
from uuid import UUID
from django.http import JsonResponse
from django.core import serializers
from .models import Wishlist

logger = logging.getLogger(__name__)

login_required
def get_wishlist_content(request):
    data = Wishlist.objects.filter(user=request.user)
    return JsonResponse(serializers.serialize("json", data), safe=False)

@login_required
@csrf_exempt
@require_http_methods(["GET"])
def get_wishlist_json(request):
    """API endpoint to get wishlist items as JSON"""
    try:
        wishlist_items = Wishlist.objects.filter(user=request.user).select_related('restaurant')
        data = []
        for item in wishlist_items:
            data.append({
                'model': 'wishlist.wishlist',
                'pk': str(item.id),
                'fields': {
                    'user': item.user.id,
                    'restaurant': str(item.restaurant.id),
                    'date_plan': item.date_plan.isoformat() if item.date_plan else None,
                    'additional_note': item.additional_note,
                    'nama_resto': item.restaurant.nama_resto,
                    'rating': item.restaurant.rating,
                    'range_harga': item.restaurant.range_harga,
                    'alamat': item.restaurant.alamat,
                }
            })
        return JsonResponse(data, safe=False)
    except Exception as e:
        logger.error(f"Error in get_wishlist_json: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@csrf_exempt
@require_http_methods(["GET", "POST"])
def add_wishlist(request, restaurant_id: UUID):
    """Handle add wishlist item with plan"""
    try:
        restaurant = get_object_or_404(RestaurantEntry, id=restaurant_id)
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            restaurant=restaurant
        )

        if request.method == 'POST':
            form = WishlistForm(request.POST, instance=wishlist_item)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'errors': form.errors})
        
        # Handle GET request - return the form HTML
        form = WishlistForm(instance=wishlist_item)
        context = {
            'form': form,
            'restaurant': restaurant
        }
        return render(request, 'add_wishlist_plan_form.html', context)
        
    except Exception as e:
        logger.error(f"Error in add_wishlist: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def toggle_wishlist(request, restaurant_id: UUID):
    """API endpoint to toggle wishlist item"""
    try:
        restaurant = get_object_or_404(RestaurantEntry, id=restaurant_id)
        wishlist_item = Wishlist.objects.filter(
            user=request.user,
            restaurant=restaurant
        ).first()
        
        if wishlist_item:
            wishlist_item.delete()
            return JsonResponse({'added': False})
        
        Wishlist.objects.create(
            user=request.user,
            restaurant=restaurant,
            date_plan=None
        )
        return JsonResponse({'added': True})
    except Exception as e:
        logger.error(f"Error in toggle_wishlist: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def delete_wishlist(request, restaurant_id: UUID):
    """API endpoint to delete wishlist item"""
    try:
        wishlist_item = get_object_or_404(
            Wishlist,
            user=request.user,
            restaurant_id=restaurant_id
        )
        wishlist_item.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        logger.error(f"Error in delete_wishlist: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@csrf_exempt
@require_http_methods(["GET", "POST"])
def edit_wishlist(request, restaurant_id: UUID):
    """API endpoint to edit wishlist item"""
    try:
        wishlist_item = get_object_or_404(
            Wishlist,
            user=request.user,
            restaurant_id=restaurant_id
        )

        if request.method == "POST":
            form = WishlistForm(request.POST, instance=wishlist_item)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'errors': form.errors})
        
        form = WishlistForm(instance=wishlist_item)
        context = {
            'form': form,
            'wishlist_item': wishlist_item
        }
        return render(request, 'edit_wishlist_plan.html', context)
        
    except Exception as e:
        logger.error(f"Error in edit_wishlist: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# Web views (for browser access)
@login_required
def show_wishlist(request):
    """Web view to show wishlist items"""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('restaurant')
    context = {
        'last_login': request.COOKIES.get('last_login', 'No recent login'),
        'wishlist_items': wishlist_items,
    }
    return render(request, 'wishlist.html', context)