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
def create_reserve_entry_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data['name']
            date = data['date']
            time = data['time']
            email = data['email']
            phone = data['phone']
            guest_quantity = data['guest_quantity']
            notes = data.get('notes', '')
            resto_id = data['resto']
            
            # Cek apakah restoran ada
            try:
                resto = RestaurantEntry.objects.get(id=resto_id)
            except RestaurantEntry.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Restaurant not found"}, status=404)
            
            # Cek apakah user ada
            user = user.objects.get(id=data['user'])

            # Simpan reservasi
            reserve_entry = ReserveEntry.objects.create(
                user=user,
                resto=resto,
                name=name,
                date=date,
                time=time,
                guest_quantity=guest_quantity,
                email=email,
                phone=phone,
                notes=notes,
            )
            return JsonResponse({"status": "success", "message": "Reservation created successfully!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

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

@require_http_methods(["POST"])
def edit_flutter(request, reservation_id):
    try:
        # Try to parse JSON data first
        data = json.loads(request.body)

        # Log the incoming data for debugging
        print(f"Received data: {data}")
        print(f"Reservation ID: {reservation_id}")

        # Fetch the reservation
        reservation = ReserveEntry.objects.get(id=reservation_id)

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

    except json.JSONDecodeError:
        # If JSON parsing fails, try form data
        try:
            # Log the incoming data for debugging
            print(f"Received POST data: {request.POST}")
            print(f"Reservation ID: {reservation_id}")

            # Fetch the reservation
            reservation = ReserveEntry.objects.get(id=reservation_id)

            # Update reservation fields
            reservation.name = request.POST.get('name')
            reservation.date = request.POST.get('date')
            reservation.time = request.POST.get('time')
            reservation.guest_quantity = request.POST.get('guest_quantity')
            reservation.email = request.POST.get('email')
            reservation.phone = request.POST.get('phone')
            reservation.notes = request.POST.get('notes', '')

            reservation.save()

            return JsonResponse({
                'success': True,
                'message': 'Reservation updated successfully'
            })

        except Exception as e:
            # Log the full exception for server-side debugging
            import traceback
            traceback.print_exc()

            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

    except ReserveEntry.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Reservation not found'
        }, status=404)
    except Exception as e:
        # Log the full exception for server-side debugging
        import traceback
        traceback.print_exc()

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

