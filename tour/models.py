from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Destination(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    place = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    image = models.ImageField()
    price_by_bus = models.CharField(max_length=20,null=True)
    price_by_Train = models.CharField(max_length=20, null=True)
    price_by_Flight = models.CharField(max_length=20, null=True)
    food_price = models.CharField(max_length=20, null=True)
    number_of_person = models.CharField(max_length=20, null=True)
    days = models.CharField(max_length=20, null=True)
    nights = models.CharField(max_length=20, null=True)
    description=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.place


class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    destination = models.ForeignKey(Destination,on_delete=models.CASCADE,null=True)
    Fname = models.CharField(max_length=30)
    Lname = models.CharField(max_length=30)
    Email = models.EmailField()
    gender = models.CharField(max_length=20,null=True)
    date = models.CharField(max_length=30,null=True)
    address = models.CharField(max_length=30,null=True)
    number = models.CharField(max_length=30,null=True)
    price = models.CharField(max_length=30,null=True)
    used_facility=models.CharField(max_length=30,null=True)

    def __str__(self):
        return self.Fname


class Contact(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    first_Name = models.CharField(max_length=30)
    last_Name = models.CharField(max_length=30)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=100)

    def __str__(self):
        return self.first_Name
