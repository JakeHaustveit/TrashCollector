from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps 
from datetime import date
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import Employee



# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.

@login_required
def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Customers = apps.get_model('customers.Customer')
    
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        
        
        all_customers= Customers.objects.all()
        logged_in_employee_zip_code= Employee.objects.get(pk=logged_in_employee.zip_code)

        today = date.today()      
    
        
        context = {
            'logged_in_employee': logged_in_employee,
            'Customer': Customers,
            'all_customers': all_customers,
            'today': today,
            'logged_in_employee_zip_code': logged_in_employee_zip_code            
        }
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))
    
    
    
    



@login_required
def create(request):
    logged_in_user = request.user
    if request.method== "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zipcode_from_form= request.POST.get('zip_code')
        new_empyloyee= Employee( name=name_from_form, user=logged_in_user, address=address_from_form, zip_code=zipcode_from_form)
        new_empyloyee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')





@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')        
        logged_in_employee.name = name_from_form
        logged_in_employee.address = address_from_form
        logged_in_employee.zip_code = zip_from_form        
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)
        



    

    



