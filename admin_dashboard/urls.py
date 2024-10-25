from django.urls import path
from admin_dashboard.views import admin_dashboard, create_menu_entry, show_xml, show_json, show_xml_by_id, show_json_by_id, menu_page, create_resto_entry, edit_menu, delete_menu, edit_resto, delete_resto

app_name = 'admin_dashboard'

urlpatterns = [
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('create-menu-entry/', create_menu_entry, name='create_menu_entry'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('menu/<uuid:pk>/', menu_page, name='menu_page'),
    path('create-resto-entry/<uuid:pk>', create_resto_entry, name='create_resto_entry'),
    path('edit_menu/<uuid:pk>', edit_menu, name='edit_menu'),
    path('edit_resto/<uuid:pk>', edit_resto, name='edit_resto'),
    path('delete_menu/<uuid:pk>', delete_menu, name='delete_menu'),
    path('delete_resto/<uuid:pk>', delete_resto, name='delete_resto'),
]
