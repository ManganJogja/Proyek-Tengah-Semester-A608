from django.urls import path
from . import views
from uuid import UUID

app_name = 'wishlist'

urlpatterns = [
    path('', views.show_wishlist, name='show_wishlist'),
    path('content/', views.get_wishlist_content, name='get_wishlist_content'),
    path('delete/<uuid:restaurant_id>/', views.delete_wishlist, name='delete_wishlist'),
    path('toggle/<uuid:restaurant_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('add/<uuid:restaurant_id>/', views.add_wishlist, name='add_wishlist'),
    path('wishlist/', views.show_wishlist, name='show_wishlist'),
]
