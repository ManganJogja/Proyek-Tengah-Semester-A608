from django.shortcuts import render, redirect, get_object_or_404
from .models import Review, Restaurant
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.contrib import messages

def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            # Check if it's an AJAX request
            if request.is_ajax():
                data = {
                    'message': 'Review submitted successfully!',
                    'review': {
                        'user': review.user.username,
                        'rating': review.rating,
                        'comment': review.comment,
                        'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    }
                }
                return JsonResponse(data)
            # Add Django messages for normal request
            messages.success(request, "Review successfully added!")
            return redirect('review_card')
        else:
            messages.error(request, "There was an error with your review.")
    else:
        form = ReviewForm()
    return render(request, 'reviews/add_review.html', {'form': form})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return JsonResponse({'message': 'Review updated successfully!'})
            return redirect('restaurant_detail', restaurant_name=review.restaurant_name)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'edit_review.html', {'form': form})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        review.delete()
        if request.is_ajax():
            return JsonResponse({'message': 'Review deleted successfully!'})
        return redirect('restaurant_detail', restaurant_name=review.restaurant_name)
    return render(request, 'delete_review.html', {'review': review})

def restaurant_detail(request, restaurant_name):
    restaurant = get_object_or_404(Restaurant, name=restaurant_name)
    reviews = Review.objects.filter(restaurant=restaurant)  # Pastikan menggunakan ForeignKey ke Restaurant
    return render(request, 'restaurant_detail.html', {
        'restaurant_name': restaurant.name,
        'restaurant_image_url': restaurant.image_url,  # Sesuaikan dengan field di model
        'restaurant_description': restaurant.description,
        'price': restaurant.price,
        'restaurant_rating': restaurant.rating,
        'restaurant_location': restaurant.location,
        'reviews': reviews
    })

def restaurant_reviews(request, restaurant_name):
    restaurant = get_object_or_404(Restaurant, name=restaurant_name)
    reviews = Review.objects.filter(restaurant=restaurant)
    return render(request, 'restaurant_reviews.html', {'restaurant_name': restaurant.name, 'reviews': reviews})

def review_card(request):
    reviews = Review.objects.all()  # Mengambil semua review
    context = {
        'reviews': reviews
    }
    return render(request, 'reviews/review_card.html', context)

def show_json(request):
    reviews = Review.objects.all()
    data = list(reviews.values('id', 'restaurant_name', 'user__username', 'rating', 'comment', 'created_at'))
    return JsonResponse(data, safe=False)

def show_json_by_id(request, id):
    try:
        review = Review.objects.get(id=id)
        data = {
            'id': review.id,
            'restaurant_name': review.restaurant_name,
            'user': review.user.username,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at,
        }
        return JsonResponse(data)
    except Review.DoesNotExist:
        raise Http404("Review not found")