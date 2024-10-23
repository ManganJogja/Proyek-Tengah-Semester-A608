from django.urls import path
from . import views

urlpatterns = [
    path('add_review/', views.add_review, name='add_review'),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    # path('reviews/<str:restaurant_name>/', views.review_card, name='restaurant_reviews'),
    path('restaurant/<str:restaurant_name>/', views.restaurant_detail, name='restaurant_detail'),
    path('reviews/json/', views.show_json, name='show_json'),
    path('reviews/json/<int:id>/', views.show_json_by_id, name='show_json_by_id'),
    path('review_card/', views.review_card, name='review_card'), # Tambahkan ini
]
