from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from order_takeaway.forms import TakeawayOrderForm
from order_takeaway.models import TakeawayOrder
from django.http import HttpResponse
from django.core import serializers
from django.utils import timezone
from django.http import JsonResponse
from admin_dashboard.models import MenuEntry, RestaurantEntry
from order_takeaway.models import TakeawayOrderItem
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


@login_required(login_url='/login')
def show_takeaway_orders(request):
    takeaway_orders = TakeawayOrder.objects.filter(user=request.user)
    context = {
        'name': request.user.username,
        'takeaway_orders': takeaway_orders
    }
    return render(request, "show_order_takeaway.html", context)

@login_required(login_url='/login')
@require_POST
@csrf_exempt
def create_takeaway_order(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Updated line
        try:
            restaurant_id = request.POST.get('restaurant')
            restaurant = RestaurantEntry.objects.get(id=restaurant_id)

            takeaway_order = TakeawayOrder(
                user=request.user,
                restaurant=restaurant,
                pickup_time=request.POST.get('pickup_time'),
                total_price=0  # This will be calculated based on items
            )
            takeaway_order.save()

            order_items = request.POST.getlist('order_items')
            quantity = int(request.POST.get('quantity', 1))

            total_price = 0
            for item_id in order_items:
                menu_item = MenuEntry.objects.get(id=item_id)
                price_per_item = restaurant.range_harga * quantity
                order_item = TakeawayOrderItem(
                    order=takeaway_order,
                    menu_item=menu_item,
                    quantity=quantity,
                    price=price_per_item
                )
                order_item.save()
                total_price += price_per_item

            takeaway_order.total_price = total_price
            takeaway_order.save()

            # Return a JSON response with the new order details
            return JsonResponse({
                "success": True,
                "id": takeaway_order.id,
                "menu": menu_item.nama_menu,
                "restaurant": restaurant.nama_resto,
                "quantity": quantity,
                "pickup_time": takeaway_order.pickup_time,
                "total_price": total_price,
            })

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"success": False, "message": "Error creating order"}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

@login_required(login_url='/login')
def edit_takeaway_order(request, id):
    order = TakeawayOrder.objects.get(pk=id)  # Get the specific order
    order_item = TakeawayOrderItem.objects.get(order=order)  # Get the related order item

    if request.method == "POST":
        form = TakeawayOrderForm(request.POST, instance=order)  # Bind POST data to the form
        if form.is_valid():
            # Save the main order
            takeaway_order = form.save(commit=False)

            # Update the related order item
            restaurant_id = request.POST.get('restaurant')
            restaurant = RestaurantEntry.objects.get(id=restaurant_id)

            # Get the new menu item from the form
            menu_id = request.POST.get('order_items')
            menu_item = MenuEntry.objects.get(id=menu_id)

            # Get the quantity from the form
            quantity = int(request.POST.get('quantity'))

            # Update the TakeawayOrderItem with the new menu, quantity, and price
            order_item.menu_item = menu_item
            order_item.quantity = quantity
            order_item.price = restaurant.range_harga * quantity
            order_item.save()

            # Update the order's total price
            takeaway_order.total_price = order_item.price
            takeaway_order.save()

            return redirect('order_takeaway:show_order_takeaway')
    else:
        # Prepopulate the form with the existing order data
        form = TakeawayOrderForm(instance=order)
    
    # Fetch all available menus to pass to the template
    menus = MenuEntry.objects.all()

    context = {
        'form': form,
        'menus': menus,
        'order_item': order_item,
        'is_edit': True,  # Flag to indicate this is the edit page
    }

    return render(request, "create_order_takeaway.html", context)  # Reuse the create template


@login_required(login_url='/login')
def delete_takeaway_order(request, id):
    order = TakeawayOrder.objects.get(pk=id)
    order.delete()
    return HttpResponseRedirect(reverse('order_takeaway:show_order_takeaway'))

def get_restaurants_by_menu(request, menu_id):
    # Fetch all restaurants that serve the selected menu
    restaurants = RestaurantEntry.objects.filter(menus__id=menu_id)  # Use `menus__id` to reference the related field
    restaurant_data = [{"id": r.id, "nama_resto": r.nama_resto} for r in restaurants]
    return JsonResponse(restaurant_data, safe=False)

@login_required
def show_json(request):
    orders = TakeawayOrder.objects.filter(user=request.user)
    response = []

    for order in orders:
        # Ambil menu, restoran, dan quantity dari order item
        try:
            order_item = TakeawayOrderItem.objects.filter(order=order).first()
            menu_name = order_item.menu_item.nama_menu if order_item else "Unknown Menu"
            quantity = order_item.quantity if order_item else 0
            restaurant_name = order.restaurant.nama_resto
        except Exception as e:
            print(f"Error fetching order details: {e}")
            menu_name = "Unknown Menu"
            quantity = 0
            restaurant_name = "Unknown Restaurant"

        response.append({
            "pk": str(order.id),  # ID order
            "fields": {
                "menu_item": menu_name,  # Nama menu
                "restaurant": restaurant_name,  # Nama restoran
                "quantity": quantity,  # Jumlah
                "pickup_time": order.pickup_time.strftime("%H:%M:%S"),  # Waktu penjemputan
                "total_price": order.total_price,  # Total harga
            }
        })

    return JsonResponse(response, safe=False)

def show_json_by_id(request, id):
    data = TakeawayOrder.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@require_GET
def get_menus(request):
    menus = MenuEntry.objects.all().values('id', 'nama_menu')
    return JsonResponse(list(menus), safe=False)

@login_required
@csrf_exempt
def create_order_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Debug log

            restaurant_id = data.get('restaurant')
            order_items = data.get('order_items', [])
            pickup_time = data.get('pickup_time')

            # Validasi data
            if not restaurant_id or not order_items or not pickup_time:
                return JsonResponse({"success": False, "message": "Incomplete data"}, status=400)

            # Parsing waktu
            try:
                formatted_time = datetime.strptime(pickup_time, "%H:%M:%S").time()
            except ValueError:
                return JsonResponse({"success": False, "message": "Invalid pickup time format"}, status=400)

            # Ambil user dari request (contoh: user pertama)
            user = User.objects.first()  # Ganti dengan user yang sesuai
            restaurant = RestaurantEntry.objects.get(id=restaurant_id)

            # Buat TakeawayOrder
            takeaway_order = TakeawayOrder(
                user=user,
                restaurant=restaurant,
                pickup_time=formatted_time,
                total_price=0  # Akan dihitung
            )
            takeaway_order.save()

            # Proses order_items
            total_price = 0
            for item in order_items:
                menu_item_id = item.get('menu_item')
                quantity = item.get('quantity', 1)

                menu_item = MenuEntry.objects.get(id=menu_item_id)

                # Hitung harga berdasarkan range_harga restoran
                price = restaurant.range_harga * quantity  # Menggunakan range_harga dari restoran

                # Buat TakeawayOrderItem
                order_item = TakeawayOrderItem(
                    order=takeaway_order,
                    menu_item=menu_item,
                    quantity=quantity,
                    price=price
                )
                order_item.save()
                total_price += price

            # Update total_price di TakeawayOrder
            takeaway_order.total_price = total_price
            takeaway_order.save()

            return JsonResponse({"success": True, "message": "Order created successfully"})

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"success": False, "message": str(e)}, status=400)

@csrf_exempt
@login_required
def edit_order_flutter(request, order_id):
    if request.method == 'POST':  # Ubah ke POST karena PUT tidak selalu didukung
        try:
            data = json.loads(request.body)
            order = get_object_or_404(TakeawayOrder, id=order_id, user=request.user)
            restaurant = get_object_or_404(RestaurantEntry, id=data['restaurant'])

            # Perbarui informasi utama order
            order.restaurant = restaurant
            order.pickup_time = data['pickup_time']
            order.total_price = 0
            order.save()

            # Hapus semua item lama
            TakeawayOrderItem.objects.filter(order=order).delete()

            # Tambahkan item baru
            total_price = 0
            for item in data.get('order_items', []):
                menu_item = get_object_or_404(MenuEntry, id=item['menu_item'])
                quantity = item.get('quantity', 1)

                # Hitung harga berdasarkan range_harga restoran
                price = restaurant.range_harga * quantity

                # Buat TakeawayOrderItem
                TakeawayOrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=quantity,
                    price=price
                )
                total_price += price

            order.total_price = total_price
            order.save()

            return JsonResponse({"success": True, "message": "Order updated successfully"})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"success": False, "message": str(e)}, status=400)

@csrf_exempt
@login_required
def delete_order_flutter(request, order_id):
    if request.method == 'POST':  # Ubah ke POST jika DELETE tidak didukung
        try:
            order = get_object_or_404(TakeawayOrder, id=order_id, user=request.user)
            order.delete()
            return JsonResponse({"status": "success"}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

# View untuk mendapatkan detail restoran berdasarkan ID
def get_restaurant_by_id(request, restaurant_id):
    restaurant = get_object_or_404(RestaurantEntry, id=restaurant_id)
    return JsonResponse({
        'id': str(restaurant.id),
        'nama_resto': restaurant.nama_resto,
        'alamat': restaurant.alamat,
        'jenis_kuliner': restaurant.jenis_kuliner,
        'lokasi_resto': restaurant.lokasi_resto,
        'range_harga': restaurant.range_harga,
        'rating': float(restaurant.rating),
        'suasana': restaurant.suasana,
        'keramaian_resto': restaurant.keramaian_resto,
    })
