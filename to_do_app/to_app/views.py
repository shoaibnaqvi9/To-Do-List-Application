from django.shortcuts import render,redirect
import re
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import User, To_do_List
from django.db import IntegrityError

def index(request):
    if request.method == 'POST':
        todo = request.POST.get('todo')
        status = request.POST.get('status')
        user = User.objects.get(id=request.session['id'])
        todo_list = To_do_List(todo=todo, status=status, user=user)
        todo_list.save()
    filter_option = request.GET.get('filter', 'all')  # Default to 'all'
    user = User.objects.get(id=request.session['id'])
    
    if filter_option == 'completed':
        todo_list = To_do_List.objects.filter(user=user, status='Completed')
    elif filter_option == 'active':
        todo_list = To_do_List.objects.filter(user=user, status='Active')
    else:
        todo_list = To_do_List.objects.filter(user=user)
    context = {
        'session_name': request.session.get('username', 'Guest'),
        'session_email': request.session.get('email', ''),
        'todo_list': todo_list,
        'filter_option': filter_option
    }
    return render(request, 'index.html', context)

def about(request):
    context = {
        'session_name': request.session.get('username', 'Guest'),
        'session_email': request.session.get('email', ''),
    }
    return render(request, 'about.html',context)

def add_task(request):
    if request.method == 'POST':
        todo = request.POST.get('todo')
        status = request.POST.get('status')
        user = User.objects.get(id=request.session['id'])
        todo_list = To_do_List(todo=todo, status=status, user=user)
        todo_list.save()
    return redirect('index')

def delete_task(request, id):
    todo_list = get_object_or_404(To_do_List, id=id)
    todo_list.delete()
    return redirect('index')

def update_task(request, id):
    todo_list = To_do_List.objects.get(id=id)
    if request.method == 'POST':
        todo_list.todo = request.POST.get('todo')
        todo_list.status = request.POST.get('status')
        todo_list.save()
        return redirect('index')
    context = {
        'task': todo_list
    }
    return redirect(request,'home',context)
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
        user = User.objects.filter(email=email, password=password)
        if user is not None:
            user = user.first()
            if user.password == password:
                request.session['id'] = user.id
                request.session['username'] = user.name
                request.session['email'] = user.email
                return redirect('index')
            else:
                messages.error(request, 'Invalid Credentials')
        else:
            messages.error(request, 'User does not exist')
    return render(request, 'login_here.html')

def logout(request):
    request.session.clear()
    return redirect('login_here')

