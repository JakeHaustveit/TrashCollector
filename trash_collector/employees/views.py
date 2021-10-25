from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps
from datetime import date

from trash_collector.employees.models import Employee

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Customer = apps.get_model('customers.Customer')
    return render(request, 'employees/index.html')



@login_required
def create(request):
    logged_in_user= request.user
    if request.method== "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zipcode_from_form= request.POST.get('zip_code')
        age_from_form = request.POST.get('age')
        new_empyloyee= Employee( name=name_from_form, address=address_from_form, zicode=zipcode_from_form, age=age_from_form)
        new_empyloyee.save()
