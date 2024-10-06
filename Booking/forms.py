from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import User
from django import forms
from django_countries.widgets import CountrySelectWidget
from select import error

from Booking.models import Profile, Booking, Payment


class CreateUserForm(UserCreationForm):

    usable_password = None
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Contraseña', required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirmar contraseña', required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'username': '',
            'email': '',
        }


class AuthForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nombre de usuario', required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Contraseña', required=True, help_text='', error_messages={'required': 'Este campo es obligatorio'})

    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['tipo_documento', 'nro_documento', 'nombre', 'apellido', 'edad', 'telefono', 'direccion', 'ciudad', 'pais', 'profile_picture']

        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control', }, choices=[('Selecciona', 'Selecciona'),('DNI', 'DNI'), ('Pasaporte', 'Pasaporte'), ('Cédula de Identidad', 'Cédula de Identidad')]),
            'nro_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': CountrySelectWidget(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class BookingForm(forms.ModelForm):

        check_in = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=True)
        check_out = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  required=True)
        adults = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='', required=True)
        children = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='', required=True)

        class Meta:
            model = Booking
            fields = ['check_in', 'check_out', 'adults', 'children']


        def clean(self):
            cleaned_data = super(BookingForm, self).clean()
            check_in = cleaned_data.get('check_in')
            check_out = cleaned_data.get('check_out')
            adults = cleaned_data.get('adults')
            children = cleaned_data.get('children')
            if Booking.objects.filter(check_in__in=[check_in, check_out], check_out__in=[check_in, check_out]).exists():
                raise forms.ValidationError('No hay habitaciones disponibles en esas fechas, cambia tus fechas e inténtalo nuevamente')
            return cleaned_data

        def __init__ (self, *args, **kwargs):
            super(BookingForm, self).__init__(*args, **kwargs)


class PaymentForm(forms.ModelForm):

    payment_method = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Metodo de pago', required=True)
    payment_amount = forms.HiddenInput(attrs={'class': 'form-control', 'value': '0.00'})

    class Meta:
        model = Payment
        fields = ['payment_method', 'payment_amount']

    def save(self, commit=True):
        payment = super(PaymentForm, self).save(commit=False)
        payment.payment_method = self.cleaned_data['payment_method']
        payment.payment_amount = self.cleaned_data['payment_amount']
        if commit:
            payment.save()
        return payment