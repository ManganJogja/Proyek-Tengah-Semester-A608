from django.urls import path
from reserve.views import *
from main.views import menu_page_user
app_name = 'reserve'

urlpatterns = [
    path('', show_reserve, name='show_reserve'),
    path('create-reserve-entry/<uuid:id>/', create_reserve_entry, name='create_reserve_entry'),
    path('confirmation-form/<uuid:id>', confirmation_form, name='confirmation_form'),
    path('edit-reserve/<uuid:id>', edit_reserve, name='edit_reserve'),
    path('delete/<uuid:id>', delete_reserve, name='delete_reserve'),
    path('json/', show_json, name='show_json'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('menu/<uuid:id>', menu_page_user, name='menu_page_user'),
]
