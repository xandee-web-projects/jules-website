from datetime import time
from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Staff, Student, User, PendingPhoto
from django.contrib import messages

# Create your views here.
def login_page(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('id'), password=request.POST.get('password'))
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('staff')
            return redirect('home')
        else:
            messages.error(request, "Incorrect ID or password")
            return redirect('login')
    return render(request, 'login.html')

@login_required
def profile(request, id):
    user = User.objects.get(username=id)
    if user:
        if user.is_superuser:
            user = request.user
        elif user.role == "student":
            user = Student.objects.get(username=id)
        elif user.role == "staff":
            user = Staff.objects.get(username=id)
    else:
        raise Http404
    return render(request, 'profile.html', {"person": user})

@login_required
def home(request):
    return profile(request, request.user.username)

def upload_photo(request, id):
    user = User.objects.filter(username=id).first()
    if user:
        try:
            user.pendingphoto.delete()
        except:
            pass
        photo = PendingPhoto(photo=request.FILES.get('photo'), user=user)
        photo.save()
    return redirect('profile', id=id)

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def forgot_password(request):
    return render(request, 'forgot-password.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def change_password(request):
    if request.method == "POST":
        former_password = request.POST.get("former")
        new_password = request.POST.get("new")
        new_password_confirm = request.POST.get("new_confirm")
        error = False
        user = authenticate(username=request.user.username, password=request.POST.get('former'))
        if not user:
            messages.error(request, "Former password is incorrect")
            error = True
        if new_password != new_password_confirm:
            messages.error(request, "New passwords has to be has to be thesame")
            error = True
        if error:
            return redirect("change_password")        
        request.user.set_password(new_password)
        request.user.save()
        login(request.user)
        messages.success(request, "Your password has been set")
    return render(request, "change-password.html")
