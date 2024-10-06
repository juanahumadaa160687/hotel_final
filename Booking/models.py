from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    check_in = models.DateField(format('%Y-%m-%d'), auto_now=False, auto_now_add=False, null=False, blank=False)
    check_out = models.DateField(format('%Y-%m-%d'), auto_now=False, auto_now_add=False, null=False, blank=False)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    adults = models.IntegerField()
    children = models.IntegerField()
    monto = models.ForeignKey('Payment', on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __int__(self):
        return self.booking_id

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_type = models.CharField(max_length=100)
    room_price = models.DecimalField(max_digits=10, decimal_places=2)
    room_capacity = models.IntegerField()
    room_availability = models.BooleanField(default=True)

    def __str__(self):
        return self.room_type

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    reserva = models.ForeignKey('Booking', on_delete=models.CASCADE, null=True, blank=True, default=None)
    payment_date = models.DateField(auto_now=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)

    def __int__(self):
        return self.payment_id

class Profile(models.Model):

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    id_cliente = models.AutoField(primary_key=True, verbose_name='ID Cliente',)

    tipo_documento = models.CharField(max_length=50, null=True, blank=True, verbose_name='Tipo de Documento')

    nro_documento = models.CharField(max_length=50, null=True, blank=True, verbose_name='Numero de Documento')

    nombre = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nombre',
                              help_text='Ingrese su nombre')
    apellido = models.CharField(max_length=50, null=False, blank=False, verbose_name='Apellido',
                                help_text='Ingrese su apellido')
    edad = models.IntegerField(null=True, blank=True, verbose_name='Edad', help_text='Ingrese su edad')

    telefono = models.CharField(max_length=15, null=True, blank=True, verbose_name='Telefono',
                                help_text='Ingrese su telefono', default='+5691324567')

    direccion = models.CharField(max_length=50, null=False, blank=False, verbose_name='Direccion',
                                 help_text='Ingrese su direccion')
    ciudad = models.CharField(max_length=50, null=False, blank=False, verbose_name='Ciudad',
                              help_text='Ingrese su ciudad')
    pais = CountryField(null=False, blank=False, verbose_name='Pais', blank_label="(Selecciona tu pais)", multiple=False)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True, verbose_name='Foto de Perfil')

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    #Profile por default
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()