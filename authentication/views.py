from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                if user.is_superuser or user.is_staff:
                    return redirect('admin_dashboard:admin_dashboard')
                else:
                    return HttpResponse(f"Login sukses untuk pengguna: {user.username}", status=200)
            else:
                return HttpResponse("Login gagal, akun dinonaktifkan.", status=403)
        else:
            return HttpResponse("Login gagal, periksa kembali email atau kata sandi.", status=401)
    
    return HttpResponse("Hanya menerima permintaan POST.", status=405)

@csrf_exempt
def logout(request):
    if request.user.is_authenticated:
        username = request.user.username
        auth_logout(request)
        return HttpResponse(f"Logout berhasil untuk pengguna: {username}", status=200)
    
    return HttpResponse("Logout gagal. Tidak ada pengguna yang login.", status=400)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return HttpResponse("Register gagal, username sudah digunakan.", status=400)

        user = User.objects.create_user(username=username, password=password)
        return HttpResponse(f"Register berhasil untuk pengguna: {user.username}", status=201)
    
    return HttpResponse("Hanya menerima permintaan POST.", status=405)
