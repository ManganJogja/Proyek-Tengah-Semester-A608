from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import MenuEntry, RestaurantEntry
from .forms import MenuEntryForm, RestaurantEntryForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers

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

def edit_product(request, id):
    menu = MenuEntry.objects.get(pk = id)
    form = MenuEntryForm(request.POST or None, instance=menu)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('admin_dashboard:admin_dashboard'))

    context = {'form': form}
    return render(request, "edit_menu.html", context)

def delete_menu(request, id):
    if not request.user.is_staff:
        return redirect('login')
    
    menu = MenuEntry.objects.get(pk=id)
    menu.delete()
    return HttpResponseRedirect(reverse('admin_dashboard:admin_dashboard'))

def edit_resto(request):
    resto = RestaurantEntry.objects.get(pk = id)
    form = RestaurantEntryForm(request.POST or None, instance=resto)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('admin_dashboard:admin_dashboard'))

def menu_page(request, no):
    menu = get_object_or_404(MenuEntry, no=no)
    restaurants = menu.restaurants.all()
    context = {
        'menu': menu,
        'restaurants': restaurants
    }
    return render(request, 'menu_page.html', context)