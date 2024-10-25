import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404
from main.models import ManganJogja
from admin_dashboard.models import MenuEntry
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@login_required(login_url='/login')
def show_main(request):
    product_entries = ManganJogja.objects.filter(user=request.user)
    menus = MenuEntry.objects.all()[91:101]
    context = {
        'app' : 'Mangan Jogja',
        'name': request.user.username,
        'last_login': request.COOKIES['last_login'],
        'product_entries': product_entries,
        'menus': menus
    }

    return render(request, "main.html", context)

def all_menus(request):
    menus = MenuEntry.objects.all() 
    context = {
        'menus': menus
    }
    return render(request, "all_menus.html", context)

def create_product_entry(request):
    form = ManganJogja(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product_entry.html", context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:
                auth_login(request, user)
                # Ini sesuaiin sama main page admin
                response = HttpResponseRedirect(reverse("admin_dashboard:admin_dashboard")) 
                response.set_cookie('last_login', str(datetime.datetime.now()))
                return response
            
            else:
                auth_login(request, user)
                response = HttpResponseRedirect(reverse("main:show_main")) 
                response.set_cookie('last_login', str(datetime.datetime.now()))
                return response
            
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    auth_logout(request)
    response = HttpResponseRedirect(reverse('main:show_main'))
    return response

def show_xml(request):
    data = ManganJogja.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = ManganJogja.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = ManganJogja.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = ManganJogja.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def menu_page_user(request, pk):
    menu = get_object_or_404(MenuEntry, pk=pk)
    restaurants = menu.restaurants.all()  # Mendapatkan semua restoran terkait dengan menu

    context = {
        'menu': menu,
        'restaurants': restaurants,
    }

    return render(request, 'menu_page_user.html', context)