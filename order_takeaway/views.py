import datetime
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
from decimal import Decimal

@login_required(login_url='/login')
def show_takeaway_orders(request):
    takeaway_orders = TakeawayOrder.objects.filter(user=request.user)
    context = {
        'name': request.user.username,
        'takeaway_orders': takeaway_orders
    }
    return render(request, "show_order_takeaway.html", context)

@login_required(login_url='/login')
def create_takeaway_order(request):
    menus = MenuEntry.objects.all()  # Load menus for the dropdown
    form = TakeawayOrderForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            # Create the initial TakeawayOrder object
            takeaway_order = form.save(commit=False)
            takeaway_order.user = request.user
            takeaway_order.order_time = timezone.now()
            takeaway_order.total_price = 0  # Initialize as an integer (or float if needed)
            takeaway_order.save()

            # Get the selected restaurant and its price (range_harga)
            restaurant_id = request.POST.get('restaurant')
            restaurant = RestaurantEntry.objects.get(id=restaurant_id)

            # Get the selected menu items and quantity
            order_items = request.POST.getlist('order_items')
            quantity = int(request.POST.get('quantity', 1))

            # For each selected menu item, create a TakeawayOrderItem
            for item_id in order_items:
                menu_item = MenuEntry.objects.get(id=item_id)

                # Use integer multiplication for price (since range_harga is an integer)
                price_per_item = restaurant.range_harga * quantity  # Integer multiplication

                # Create the order item
                order_item = TakeawayOrderItem(
                    order=takeaway_order,
                    menu_item=menu_item,
                    quantity=quantity,
                    price=price_per_item  # Set the price as an integer
                )
                order_item.save()

                # Update the total price for the order
                takeaway_order.total_price += price_per_item

            # Save the final order with the updated total price
            takeaway_order.save()

            # Redirect to show_order_takeaway page
            return redirect('order_takeaway:show_order_takeaway')

    context = {
        'form': form,
        'menus': menus,
    }

    return render(request, "create_order_takeaway.html", context)

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

def show_json(request):
    data = TakeawayOrder.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = TakeawayOrder.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
