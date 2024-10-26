from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import MenuEntry, RestaurantEntry
from .forms import MenuEntryForm, RestaurantEntryForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
import uuid

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('login')

    menus = MenuEntry.objects.all()
    context = {
        'name': request.user.username,
        'menus' : menus
    }

    return render(request, 'admin_dashboard.html', context)

def create_menu_entry(request):
    form = MenuEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        menu_entry = form.save(commit=False)
        menu_entry.save()
        return redirect('admin_dashboard:admin_dashboard')

    context = {'form': form}
    return render(request, "create_menu_entry.html", context)

def show_xml(request):
    data = MenuEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = MenuEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = MenuEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = MenuEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def edit_menu(request, pk):
    menu = MenuEntry.objects.get(pk=pk)
    form = MenuEntryForm(request.POST or None, instance=menu)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('admin_dashboard:admin_dashboard'))

    context = {'form': form}
    return render(request, "edit_menu.html", context)

def delete_menu(request, pk):
    if not request.user.is_staff:
        return redirect('login')
    
    menu = MenuEntry.objects.get(pk=pk)
    related_restaurants = list(menu.restaurants.all())
    menu.delete() 

    for restaurant in related_restaurants:
        if restaurant.menus.count() == 0:  # cek restoran tidak memiliki menu lain
            restaurant.delete()

    return HttpResponseRedirect(reverse('admin_dashboard:admin_dashboard'))

def edit_resto(request, pk):
    resto = RestaurantEntry.objects.get(pk=pk)
    form = RestaurantEntryForm(request.POST or None, instance=resto)

    if form.is_valid() and request.method == "POST":
        form.save()

        # ambil menu yang terkait dengan restoran ini
        menu = resto.menus.first()  # ambil menu pertama yang terkait dengan resto
        return HttpResponseRedirect(reverse('admin_dashboard:menu_page', args=[menu.id]))
    
    context = {'form': form, 'resto': resto}
    return render(request, "edit_resto.html", context)


def menu_page(request, pk):
    menu = get_object_or_404(MenuEntry, pk=pk)
    restaurants = menu.restaurants.all()
    context = {
        'menu': menu,
        'restaurants': restaurants
    }
    return render(request, 'menu_page.html', context)

def create_resto_entry(request, pk):
    form = RestaurantEntryForm(request.POST or None)
    menu = get_object_or_404(MenuEntry, pk=pk)

    if form.is_valid() and request.method == "POST":
        resto_entry = form.save() 
        menu.restaurants.add(resto_entry)
        
        return redirect('admin_dashboard:menu_page', pk=pk)

    context = {'form': form, 'menu': menu}
    return render(request, "create_resto_entry.html", context)


def delete_resto(request, pk):
    if not request.user.is_staff:
        return redirect('login')
    
    resto = get_object_or_404(RestaurantEntry, pk=pk)
    menu = resto.menus.first()
    
    resto.delete()
    
    return HttpResponseRedirect(reverse('admin_dashboard:menu_page', args=[menu.id]))

def all_menus_admin(request):
    menus = MenuEntry.objects.all() 
    context = {
        'menus': menus
    }
    return render(request, "all_menus_admin.html", context)

def restaurants_admin(request):
    restaurants = RestaurantEntry.objects.all()  
    return render(request, 'restaurants_admin.html', {'restaurants': restaurants})