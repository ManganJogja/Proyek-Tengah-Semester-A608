from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.contrib import messages

@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
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
            return redirect('review_card')  # Redirect setelah update
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'reviews/edit_review.html', {'form': form, 'review': review})  # Kirim objek 'review'

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

def review_card(request):
    reviews = Review.objects.all()
    return render(request, 'reviews/review_card.html', {'reviews': reviews})

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
