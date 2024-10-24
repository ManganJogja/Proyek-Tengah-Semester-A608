import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from reserve.forms import ReserveEntryForm
from reserve.models import ReserveEntry
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

def require_previous_page(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('confirmation_form', False):
            return redirect(reverse('confirmation_form'))  
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

def show_reserve(request):
    request.session['confirmation_form'] = False
    print(request.session.get('confirmation_form'))
    reserve_entries = ReserveEntry.objects.filter(user=request.user)
    context = {  
        'name': request.user.username,
        'reserve_entries': reserve_entries
    }

    return render(request, "reserve_page.html", context)

@login_required(login_url='/login')
def create_reserve_entry(request):
    if request.session.get('confirmation_form') == False:
        print('halo')
        return redirect('reserve:confirmation_form')

    form = ReserveEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        reserve_entry = form.save(commit=False)
        reserve_entry.user = request.user
        reserve_entry.save()
        return redirect('reserve:show_reserve')
    
    print('hala')
    context = {'form': form}
    return render(request, "create_reserve_entry.html", context)
    
def confirmation_form(request):
    request.session['confirmation_form'] = True
    return render(request, "confirmation_form.html")

def edit_reserve(request, id):
    reserve = ReserveEntry.objects.get(pk = id)
    form = ReserveEntryForm(request.POST or None, instance=reserve)
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('reserve:show_reserve'))

    context = {'form': form,
               'reserve':reserve}
    return render(request, "edit_reserve.html", context)

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