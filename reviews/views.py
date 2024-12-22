import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import reviews
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.contrib import messages
from admin_dashboard.models import RestaurantEntry
from django.contrib.auth.models import User
import logging
import traceback

logger = logging.getLogger(__name__)

@csrf_exempt
@login_required
def add_review(request, restaurant_id):
    restaurant = get_object_or_404(RestaurantEntry, id=restaurant_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        user = request.user

        # Pastikan data rating dan comment ada
        if rating and comment:
            # Buat review baru
            review = Review.objects.create(
                restaurant=restaurant,
                user=request.user,
                rating=rating,
                comment=comment
            )
            review.save()

            # Redirect ke halaman review card setelah review ditambahkan
            return redirect('reviews:review_card', restaurant_id=restaurant.id)
    return render(request, 'add_review.html', {'restaurant': restaurant})

@csrf_exempt
@login_required
def edit_review(request, review_id):
    # Ambil review berdasarkan ID dan pastikan review dimiliki oleh user yang login
    review = get_object_or_404(Review, id=review_id, user=request.user)
    restaurant = review.restaurant  # Ambil restoran yang terkait dengan review

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Update review dengan data baru
        review.rating = rating
        review.comment = comment
        review.save()

        # Redirect ke halaman review card restoran setelah review diubah
        return redirect('reviews:review_card', restaurant_id=restaurant.id)
    return render(request, 'edit_review.html', {'review': review})

@csrf_exempt
@login_required
def delete_review(request, review_id):
    if request.method == 'POST':
        try:
            review = get_object_or_404(Review, id=review_id, user=request.user)
            review.delete()

            # Cek apakah ini permintaan AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Review deleted successfully!'})

            # Jika bukan AJAX, redirect ke halaman lain
            return redirect('reviews:review_card', restaurant_id=review.restaurant.id)
        except Review.DoesNotExist:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Review not found!'}, status=404)
            return redirect('reviews:review_card', restaurant_id=review.restaurant.id)

    return JsonResponse({'message': 'Invalid request'}, status=400)

def review_card(request, restaurant_id):
    # Ambil restoran berdasarkan UUID
    restaurant = get_object_or_404(RestaurantEntry, id=restaurant_id)
    
    # Ambil semua review untuk restoran tersebut
    reviews = Review.objects.filter(restaurant=restaurant)
    
    # Sorting berdasarkan request parameter
    sort_option = request.GET.get('sort', 'default')

    if sort_option == 'highest':
        reviews = reviews.order_by('-rating')  # tertinggi ke terendah
    elif sort_option == 'lowest':
        reviews = reviews.order_by('rating')  # terendah ke tertinggi
    elif sort_option in ['5', '4', '3', '2', '1']:
        reviews = reviews.filter(rating=sort_option)  # filter sesuai rating bintang
    
    # Render template review_card.html dengan context
    return render(request, 'review_card.html', {'restaurant': restaurant, 'reviews': reviews, 'sort_option': sort_option})

def show_json(request):
    reviews = Review.objects.all()
    data = list(reviews.values('id', 'user__username', 'rating', 'comment', 'created_at'))
    return JsonResponse(data, safe=False)

def show_json_by_id(request, restaurant_id):
    try:
        reviews = Review.objects.filter(restaurant_id=restaurant_id)
        if not reviews.exists():  # Jika tidak ada review
            return JsonResponse({'reviews': [], 'message': 'No reviews found'}, status=200)

        data = {
            'reviews': list(reviews.values('id', 'user__username', 'rating', 'comment', 'created_at'))
        }
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)

# VERSI FLUTTER

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from functools import wraps
import logging
logger = logging.getLogger(__name__)

def login_required_json(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": False,
                "message": "User not authenticated"
            }, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

@csrf_exempt
@login_required_json
def add_review_flutter(request, restaurant_id):
    if request.method == 'POST':
        try:
            restaurant = get_object_or_404(RestaurantEntry, id=restaurant_id)
            
            # Parse data
            data = request.POST
            rating = data.get('rating')
            comment = data.get('comment')
            
            if not all([rating, comment]):
                return JsonResponse({
                    'status': 'error',
                    'error': 'Rating and comment are required'
                }, status=400)
            
            # Create review menggunakan request.user langsung
            review = Review.objects.create(
                restaurant=restaurant,
                user=request.user,
                rating=int(rating),
                comment=comment
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Review added successfully!'
            })
            
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            logger.error(traceback.format_exc())
            return JsonResponse({
                'status': 'error',
                'error': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'error': 'Invalid request method'
    }, status=405)
    
@csrf_exempt
@login_required_json
def edit_review_review(request, review_id):
    if request.method == 'POST':
        try:
            review = get_object_or_404(Review, id=review_id, user=request.user)
            
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')
            
            if not all([rating, comment]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Rating and comment are required'
                }, status=400)
                
            review.rating = int(rating)
            review.comment = comment
            review.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Review updated successfully'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
            
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

@csrf_exempt
@login_required
def delete_review_flutter(request, review_id):
    if request.method == 'POST':  # Gunakan POST untuk menghapus data
        try:
            review = Review.objects.get(id=review_id)
            review.delete()
            return JsonResponse({"status": "success", "message": "Review deleted successfully"})
        except Review.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Review not found"}, status=404)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@csrf_exempt
def get_reviews(request, restaurant_id):
    if request.method == 'GET':
        reviews = Review.objects.filter(restaurant_id=restaurant_id)
        review_list = list(reviews.values('id', 'user__username', 'rating', 'comment', 'created_at'))
        return JsonResponse({
            "reviews": review_list,
            "status": "success"
        }, safe=False)
    
