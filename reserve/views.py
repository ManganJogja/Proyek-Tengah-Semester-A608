from datetime import date
from django.db.models import Sum, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404
from reserve.forms import ReserveEntryForm
from reserve.models import ReserveEntry
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.html import strip_tags
from admin_dashboard.models import RestaurantEntry, MenuEntry
from django.contrib import messages
from main.views import show_main


@login_required(login_url='/login')
def show_reserve(request):
    # Ambil nama restoran dari query parameter
    restaurant_name = request.GET.get('restaurant', '').strip()

    # Ambil semua reservasi milik user yang login
    reserve_entries = ReserveEntry.objects.filter(user=request.user)

    # Jika ada nama restoran yang dipilih, filter berdasarkan restoran tersebut
    if restaurant_name:
        reserve_entries = reserve_entries.filter(resto__nama_resto__icontains=restaurant_name)

    # Ambil daftar semua restoran
    restaurants = RestaurantEntry.objects.values('nama_resto').distinct()

    context = {
        'name': request.user.username,
        'reserve_entries': reserve_entries,
        'restaurants': restaurants,
        'selected_restaurant': restaurant_name,  # Untuk menjaga pilihan di dropdown
    }

    return render(request, "reserve_page.html", context)


@login_required(login_url='/login')
def create_reserve_entry(request, id):
    restaurant = get_object_or_404(RestaurantEntry, pk=id)
    form = ReserveEntryForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            reserve_entry = form.save(commit=False)
            guest_quantity = form.cleaned_data['guest_quantity']
            selected_date = form.cleaned_data['date']

            # Hitung tamu yang sudah ada untuk tanggal yang dipilih
            total_guests_selected_date = ReserveEntry.objects.filter(
                resto=restaurant,
                date=selected_date
            ).aggregate(total_guests=Sum('guest_quantity'))['total_guests'] or 0

            if total_guests_selected_date + guest_quantity > 100:
                messages.error(request, 'Sorry, the restaurant is fully booked')
                return redirect('reserve:create_reserve_entry', id=id)
            else:
                reserve_entry.user = request.user
                reserve_entry.resto = restaurant
                reserve_entry.save()
                return redirect('reserve:show_reserve')

    context = {'form': form, 'restaurant': restaurant}
    return render(request, "create_reserve_entry.html", context)

def confirmation_form(request, id):
    restaurant = get_object_or_404(RestaurantEntry, pk=id)
    
    if request.method == "POST":
        return redirect('reserve:create_reserve_entry', id=id)
    
    context = {'restaurant': restaurant}
    return render(request, "confirmation_form.html", context)

@csrf_exempt
@require_http_methods(["GET", "POST"])  
def edit_reserve(request, id):
    reserve_entry = get_object_or_404(ReserveEntry, pk=id, user=request.user)  # Ambil objek tunggal

    if request.method == 'GET':
        data = {
            'guest_quantity': reserve_entry.guest_quantity,
            'notes': reserve_entry.notes,
        }
        return JsonResponse(data)
    elif request.method == 'POST':
        name = request.POST.get("name")
        date = request.POST.get("date")
        time = request.POST.get("time")
        guest_quantity = request.POST.get("guest_quantity")
        notes = request.POST.get('notes')
        new_reserve = ReserveEntry(
            notes=notes, guest_quantity=guest_quantity, name=name, time=time, date=date
        )
        new_reserve.save()
        return HttpResponse(b"CREATED", status=201)
def delete_reserve(request, id):
    reserve = ReserveEntry.objects.get(pk = id)
    reserve.delete()
    return HttpResponseRedirect(reverse('reserve:show_reserve'))

def show_json(request):
    data = ReserveEntry.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = ReserveEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

