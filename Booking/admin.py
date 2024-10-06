from django.contrib import admin
from django.contrib.auth.models import User

from Booking.models import Profile, Booking, Room, Payment

admin.site_header = 'Hotel Pacific Reef'
admin.site_title = 'Hotel Pacific Reef'
admin.index_title = 'Bienvenido a Hotel Pacific Reef'

admin.site.register(Profile)
admin.site.register(Booking)
admin.site.register(Room)
admin.site.register(Payment)


