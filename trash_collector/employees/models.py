from django.db import models

# Create your models here.

# TODO: Create an Employee model with properties required by the user stories

class Employee(models.Model):
    name= models.CharField( max_length=50)
    address= models.CharField( max_length=200)
    zipcode= models.IntegerField(max_length=10)
    age= models.DateField(null=True, blank=True)
