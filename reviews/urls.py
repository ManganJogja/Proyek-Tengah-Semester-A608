from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'reviews'

urlpatterns = [
    path('add_review/<uuid:restaurant_id>/', views.add_review, name='add_review'),
    path('card/<uuid:restaurant_id>/', views.review_card, name='review_card'),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('restaurant/<uuid:restaurant_id>/', views.review_card, name='review_card'),
    path('reviews/json/', views.show_json, name='show_json'),
    path('reviews/json/<uuid:restaurant_id>/', views.show_json_by_id, name='show_json_by_id'),
    path('add_review_flutter/<uuid:restaurant_id>/', views.add_review_flutter, name='add_review_flutter'),
    path('edit_review_flutter/<int:review_id>/', views.edit_review_review, name='edit_review_flutter'),
    path('delete_review_flutter/<int:review_id>/', views.delete_review_flutter, name='delete_review_flutter'),
    # path('current_user/', views.current_user, name='current_user'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('restaurant/<uuid:restaurant_id>/json/', views.show_json_by_id, name='show_json_by_id'),
]
