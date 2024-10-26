from django.urls import path
from . import views

urlpatterns = [
    path('add_review/<uuid:restaurant_id>/', views.add_review, name='add_review'),
    path('reviews/card/<uuid:restaurant_id>/', views.review_card, name='review_card'),  # Ini seharusnya mengarah ke views.review_card
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('restaurant/<uuid:restaurant_id>/', views.review_card, name='review_card_by_restaurant'),
    path('reviews/json/', views.show_json, name='show_json'),
    path('reviews/json/<int:id>/', views.show_json_by_id, name='show_json_by_id'),
]
