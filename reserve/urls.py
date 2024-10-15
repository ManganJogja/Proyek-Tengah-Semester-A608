from django.urls import path
from reserve.views import *

app_name = 'reserve'

urlpatterns = [
    path('', show_main, name='show_main'),
]