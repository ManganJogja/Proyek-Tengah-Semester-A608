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

@login_required(login_url='/login')
def show_takeaway_orders(request):
    takeaway_orders = TakeawayOrder.objects.filter(user=request.user)
    context = {
        'name': request.user.username,
        'takeaway_orders': takeaway_orders
    }
    return render(request, "takeaway_orders_page.html", context)

@login_required(login_url='/login')
def create_takeaway_order(request):
    form = TakeawayOrderForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        takeaway_order = form.save(commit=False)
        takeaway_order.user = request.user
        takeaway_order.order_time = timezone.now()  # Add order timestamp
        takeaway_order.save()
        return redirect('takeaway:show_takeaway_orders')

    context = {'form': form}
    return render(request, "create_takeaway_order.html", context)

@login_required(login_url='/login')
def edit_takeaway_order(request, id):
    order = TakeawayOrder.objects.get(pk=id)
    form = TakeawayOrderForm(request.POST or None, instance=order)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('takeaway:show_takeaway_orders'))

    context = {'form': form}
    return render(request, "edit_takeaway_order.html", context)

@login_required(login_url='/login')
def delete_takeaway_order(request, id):
    order = TakeawayOrder.objects.get(pk=id)
    order.delete()
    return HttpResponseRedirect(reverse('takeaway:show_takeaway_orders'))

@login_required(login_url='/login')
def show_takeaway_orders_json(request):
    data = TakeawayOrder.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url='/login')
def show_takeaway_order_json_by_id(request, id):
    data = TakeawayOrder.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
