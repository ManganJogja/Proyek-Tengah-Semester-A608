from django.urls import path
from main.views import show_main, register, login_user, logout_user
from main.views import show_json, show_xml, show_xml_by_id, show_json_by_id, menu_page_user, all_menus

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),   
    path('json/', show_json, name='show_json'),
    path('xml/', show_xml, name='show_xml'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('menu/<uuid:pk>/', menu_page_user, name='menu_page_user'),
    path('all-menus/', all_menus, name='all_menus'),

]