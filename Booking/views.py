from urllib.request import Request

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.views.decorators.csrf import csrf_exempt
import datetime

from django.contrib.auth.decorators import login_required

from Booking.forms import AuthForm, CreateUserForm, ProfileForm, BookingForm, PaymentForm
from Booking.models import Booking, Room

@login_required(login_url='login')
@csrf_exempt
def booking(request):



    c_in = request.POST['checkin']
    c_out = request.POST['checkout']
    room_type = request.POST['type_room']
    adult = request.POST['adults']
    child = request.POST['children']
    persons = int(adult) + int(child)
    print(c_in)
    print(c_out)
    print(room_type)
    print(adult)
    print(child)
    print(persons)



    if Booking.objects.filter(check_in__in=[c_in, c_out], check_out__in=[c_in, c_out]).exists():

        messages.error(request, 'No hay habitaciones disponibles en esas fechas, cambia tus fechas e inténtalo nuevamente')

        return render(request, 'index.html')

    else:

        roooms=Room.objects.filter(room_type=room_type, room_capacity__gte=persons, room_availability=True).distinct().all()



        booking_form=BookingForm(request.POST)
        if booking_form.is_valid():

            booking_form.save(commit=False)
            booking_form.room=roooms
            booking_form.check_in=c_in
            booking_form.check_out=c_out
            booking_form.adults=adult
            booking_form.children=child

            booking_form.save()

        print(roooms)

        return render(request, 'booking.html', {'roooms': roooms, 'checkin': c_in, 'checkout': c_out, 'booking_form': booking_form})



def rooms(request):
    return render(request, 'rooms.html')

def payment(request):

    if request.method == 'POST':
        form = PaymentForm(request.POST)


        hab_id = request.session.get('room_id')
        room_price = request.session.get('room_price')

        c_in = request.session.get('check_in')

        c_out = request.session.get('check_out')
        estadia = datetime.datetime.strptime(c_out, '%Y-%m-%d') - datetime.datetime.strptime(c_in, '%Y-%m-%d')
        estadia = estadia.days

        total_estadia = estadia * room_price

        impuesto = total_estadia * 0.19

        total = total_estadia + impuesto

        reserva = total * 0.3

        if form.is_valid():


            form.save(commit=False)
            form.payment_method = request.POST.get('payment_method')
            form.booking = hab_id
            form.payment_amount = total

            form.save()
            Room.objects.filter(room_id=hab_id).update(room_availability=False)
            return render(request, 'payment.html', {'total': total, 'impuesto': impuesto, 'reserva': reserva, 'room_price': room_price, 'checkin': c_in, 'checkout': c_out, 'estadia': estadia, 'form': form})


    return render(request, 'payment.html')

def login_user(request):
    if request.method == 'POST':
        form = AuthForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        else:
            messages.error(request, 'Error al crear el usuario')

    return render(request, 'register.html')
def index(request):

    booking_form = BookingForm(request.POST)
    if booking_form.is_valid():
        booking_form.save()
    return render(request, 'index.html', {'booking_form': booking_form})

def logout_user(request):
    logout(request)
    redirect('index')
    return render(request, 'index.html')

def premium(request):
    return render(request, 'premium.html')

def turista(request):
    return render(request, 'turista.html')

def profile(request):

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('payment')
        else:
            messages.error(request, 'Error al actualizar el perfil')

    return render(request, 'payment.html')