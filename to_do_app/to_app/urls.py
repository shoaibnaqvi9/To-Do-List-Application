from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('signup_here/', views.signup, name='signup_here'),
    path('login_here/', views.login, name='login_here'),
    path('logout/', views.logout, name='logout'),
    path('delete/<int:id>/', views.delete_task, name='delete_task'),
    path('update/<int:id>/', views.update_task, name='update_task'),
]
