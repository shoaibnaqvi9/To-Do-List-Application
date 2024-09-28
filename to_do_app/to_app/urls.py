from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.index, name = 'index'),
    path('signup_here/', views.signup, name = 'signup_here'),
    path('login_here/', views.login, name = 'login_here'),
]