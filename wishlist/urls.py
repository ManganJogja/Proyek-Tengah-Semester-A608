from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.show_wishlist, name='show_wishlist'),
    path('add/', views.add_wishlist, name='add_wishlist'),
    # path('add/<uuid:restaurant_id>/', views.add_wishlist, name='add_wishlist'),
    path('delete/<uuid:restaurant_id>/', views.delete_wishlist, name='delete_wishlist'),
]