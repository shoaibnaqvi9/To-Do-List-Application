from django.shortcuts import render,redirect
import re
from django.contrib import messages
from .models import User, To_do_List

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get['username']
        email = request.POST.get['email']
        password = request.POST.get['password']
        confirm_password = request.POST.get['confirm_password']
        password_regex = re.compile(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
        if not password_regex.match(password):
            messages.error(request, "Password must be at least 8 characters long, include 1 uppercase letter, 1 number, and 1 special character.")
            return render(request, "signup_here.html")
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup_here.html")
        user = User(username=username, email=email, password=password)
        user.save()
        return redirect('login_here')

def login(request):
    if request.method == 'POST':
        email = request.POST.get['email']
        password = request.POST.get['password']
        user = User.objects.filter(email=email)
        if user is not None:
            user = user[0]
            if user.password == password:
                request.session['user_id'] = user.id
                request.session['name'] = user.name
                request.session['email'] = user.email
                return redirect('dashboard')
            else:
                msg = 'Invalid Credentials'
                messages.error(request, msg)
                return render(request, 'login_here.html', {'msg': msg})
    else:
        return render(request, 'login_here.html')

def logout(request):
    logout(request)
    return redirect('login')
