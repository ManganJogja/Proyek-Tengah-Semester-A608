from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404

@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
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
            return redirect('restaurant_reviews', restaurant_name=form.cleaned_data['restaurant_name'])
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form})

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
    reviews = Review.objects.filter(restaurant_name=restaurant_name)
    return render(request, 'restaurant_detail.html', {'restaurant_name': restaurant_name, 'reviews': reviews})

def restaurant_reviews(request, restaurant_name):
    reviews = Review.objects.filter(restaurant_name=restaurant_name)
    return render(request, 'restaurant_reviews.html', {'restaurant_name': restaurant_name, 'reviews': reviews})

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