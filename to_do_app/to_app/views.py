from django.shortcuts import render,redirect
import re
from django.contrib import messages
from .models import User, To_do_List
from django.db import IntegrityError

def index(request):
    if 'id' in request.session:
        name= request.session.get('name')
        return render(request, 'index.html', {'name': name})

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        password_regex = re.compile(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
        if not password_regex.match(password):
            messages.error(request, "Password must be at least 8 characters long, include 1 uppercase letter, 1 number, and 1 special character.")
            return render(request, "signup_here.html")
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup_here.html")
        if not name or not email or not password:
            messages.error(request, "All fields are required.")
            print(name,email,password,confirm_password)
        try:
            user = User(name=name, email=email, password=password)
            user.save()
            return redirect('login_here')
        except IntegrityError:
            messages.error(request, "This email is already registered.")
            return render(request, "signup_here.html")
    return render(request, 'signup_here.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email)
        if user is not None:
            user = user[0]
            if user.password == password:
                request.session['id'] = user.id
                request.session['username'] = user.name
                request.session['email'] = user.email
                return redirect('index')
            else:
                msg = 'Invalid Credentials'
                messages.error(request, msg)
        else:
            messages.error(request, 'User does not exist')
    return render(request, 'login_here.html')

def logout(request):
    request.session.clear()
    return redirect('login_here')