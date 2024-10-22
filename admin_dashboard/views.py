from django.shortcuts import render, redirect, reverse
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