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
import json
from django.views.decorators.http import require_POST



@login_required(login_url='/login')
def show_reserve(request):
    restaurant_name = request.GET.get('restaurant', '').strip()

    reserve_entries = ReserveEntry.objects.filter(user=request.user)

    if restaurant_name:
        reserve_entries = reserve_entries.filter(resto__nama_resto__icontains=restaurant_name)

    restaurants = RestaurantEntry.objects.values('nama_resto').distinct()

    context = {
        'name': request.user.username,
        'reserve_entries': reserve_entries,
        'restaurants': restaurants,
        'selected_restaurant': restaurant_name, 
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

@csrf_exempt
def create_reserve_entry_flutter(request, restoId):
    if request.method == 'GET':
        try:
            # Retrieve restaurant details or return basic info
            resto = RestaurantEntry.objects.get(id=restoId)
            return JsonResponse({
                "status": "success", 
                "resto_name": resto.nama_resto,
                "resto_id": str(resto.id)
            })
        except RestaurantEntry.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Restaurant not found"})
    
    if request.method == 'POST':
        # Existing POST method logic remains the same
        try:
            data = json.loads(request.body)
            resto = RestaurantEntry.objects.get(id=restoId)
            
            user = request.user  # Replace with actual user retrieval
            
            reserve_entry = ReserveEntry.objects.create(
                user=user,
                resto=resto,
                name=data['name'],
                date=data['date'],
                time=data['time'],
                guest_quantity=int(data['guest_quantity']),
                email=data['email'],
                phone=data['phone'],
                notes=data.get('notes', ''),
            )
            return JsonResponse({"status": "success", "message": "Reservation created successfully!"})
        
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    
    return JsonResponse({"status": "error", "message": "Method not allowed"})
   
def confirmation_form(request, id):
    restaurant = get_object_or_404(RestaurantEntry, pk=id)
    
    if request.method == "POST":
        return redirect('reserve:create_reserve_entry', id=id)
    
    context = {'restaurant': restaurant}
    return render(request, "confirmation_form.html", context)

@csrf_exempt
@require_http_methods(["GET", "POST"])  
def edit_reserve(request, id):
    reserve = get_object_or_404(ReserveEntry, pk=id)
    if request.method == 'POST':
        form = ReserveEntryForm(request.POST, instance=reserve)
        if form.is_valid():
            form.save()
            return redirect('reserve:show_reserve')

@require_http_methods(["GET", "POST"])
@csrf_exempt
def edit_flutter(request, id):
    try:
        if request.method == "GET":
            reservation = ReserveEntry.objects.get(id=id)
            
            return JsonResponse({
                'success': True,
                'data': {
                    'name': reservation.name,
                    'date': reservation.date,
                    'time': reservation.time,
                    'guest_quantity': reservation.guest_quantity,
                    'email': reservation.email,
                    'phone': reservation.phone,
                    'notes': reservation.notes,
                }
            })

        elif request.method == "POST":
            data = json.loads(request.body)
     
            reservation = ReserveEntry.objects.get(id=id)

            # Update reservation fields
            reservation.name = data.get('name')
            reservation.date = data.get('date')
            reservation.time = data.get('time')
            reservation.guest_quantity = data.get('guest_quantity')
            reservation.email = data.get('email')
            reservation.phone = data.get('phone')
            reservation.notes = data.get('notes', '')

            reservation.save()

            return JsonResponse({
                'success': True,
                'message': 'Reservation updated successfully'
            })


    except Exception as e:
        print("Error:", e)
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
     
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

@csrf_exempt
def delete_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reserve_pk = data.get("pk")
            
            reserve = ReserveEntry.objects.get(pk=reserve_pk)
            reserve.delete()
            
            return JsonResponse({
                "status": "success",
                "message": 'Reservation successfully deleted',
            }, status=200)
        
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e),
            }, status=500)
    
    return JsonResponse({
        "status": "error",
        "message": 'Invalid request method',
    }, status=405)