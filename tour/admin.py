from django.contrib import admin
from .models import*

# Register your models here.

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['id','place','country','image','price_by_bus','price_by_Train','price_by_Flight',]

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id','user','Fname','Lname','Email','gender','destination']

@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ['id','user','first_Name','last_Name','email','subject','message']
