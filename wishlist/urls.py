from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_wishlist, name='show_wishlist'),
]

