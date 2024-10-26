from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.contrib import messages
from admin_dashboard.models import RestaurantEntry

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
                user=user,
                rating=rating,
                comment=comment
            )
            review.save()

            # Redirect ke halaman review card setelah review ditambahkan
            return redirect('reviews:review_card', restaurant_id=restaurant.id)
    return render(request, 'add_review.html', {'restaurant': restaurant})

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
            return redirect('review_card')

        except Review.DoesNotExist:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Review not found!'}, status=404)
            return redirect('review_card')

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

def show_json_by_id(request, id):
    try:
        review = Review.objects.get(id=id)
        data = {
            'id': review.id,
            'user': review.user.username,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at,
        }
        return JsonResponse(data)
    except Review.DoesNotExist:
        raise Http404("Review not found")
