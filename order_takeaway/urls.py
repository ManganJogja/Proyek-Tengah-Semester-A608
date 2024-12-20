from django.urls import path
from reserve.views import *
from order_takeaway.views import show_takeaway_orders, create_takeaway_order, edit_takeaway_order, delete_takeaway_order, show_json, show_json_by_id, get_restaurants_by_menu, get_menus
from order_takeaway.views import create_order_flutter, edit_order_flutter, delete_order_flutter, get_restaurant_by_id

app_name = 'order-takeaway'

urlpatterns = [
    path('show-order-takeaway/', show_takeaway_orders, name='show_order_takeaway'),  
    path('create-order-takeaway/', create_takeaway_order, name='create_order_takeaway'),  
    path('edit-order-takeaway/<uuid:id>/', edit_takeaway_order, name='edit_order_takeaway'),  
    path('delete-order-takeaway/<uuid:id>/', delete_takeaway_order, name='delete_order_takeaway'), 
    path('json/', show_json, name='show_json'),  
    path('json/<uuid:id>/', show_json_by_id, name='show_json_by_id'),  
    path('api/restaurants/<uuid:menu_id>/', get_restaurants_by_menu, name='get_restaurants_by_menu'),
    path('api/menus/', get_menus, name='get_menus'),
    path('api/order/create/', create_order_flutter, name='create_order_flutter'),
    path('api/order/edit/<uuid:order_id>/', edit_order_flutter, name='edit_order_flutter'),
    path('api/order/delete/<uuid:order_id>/', delete_order_flutter, name='delete_order_flutter'),
    path('api/restaurant/<uuid:restaurant_id>/', get_restaurant_by_id, name='get_restaurant_by_id'),
]