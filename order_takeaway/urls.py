from django.urls import path
from reserve.views import *
from order_takeaway.views import show_takeaway_orders, create_takeaway_order, edit_takeaway_order, delete_takeaway_order, show_json, show_json_by_id


app_name = 'order_takeaway'

urlpatterns = [
    path('', show_takeaway_orders, name='show_takeaway_orders'),  
    path('create/', create_takeaway_order, name='create_takeaway_order'),  
    path('edit/<uuid:id>/', edit_takeaway_order, name='edit_takeaway_order'),  
    path('delete/<uuid:id>/', delete_takeaway_order, name='delete_takeaway_order'), 
    path('json/', show_json, name='show_json'),  
    path('json/<uuid:id>/', show_json_by_id, name='show_json_by_id'),  
]