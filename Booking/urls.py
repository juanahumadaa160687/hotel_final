from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('booking/', views.booking, name='booking'),
    path('rooms/', views.rooms, name='rooms'),
    path('payment/', views.payment, name='payment'),
    path('login_user/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout_user/', views.logout, name='logout'),
    path('premium/', views.premium, name='premium'),
    path('turista/', views.turista, name='turista'),
]