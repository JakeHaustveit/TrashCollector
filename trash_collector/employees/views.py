from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps 
from datetime import date 
import calendar
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import Employee
from django.db.models import Q


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
        date_numbers = date.today()
        day_of_week= calendar.day_name[date_numbers.weekday()] 

         
        customer_matching_zip_code= all_customers.filter(zip_code= logged_in_employee.zip_code)
        
        customer_active_account= customer_matching_zip_code.filter(Q(suspend_end__lt = date_numbers, suspend_start__gt= date_numbers) | Q(suspend_end__isnull=True, suspend_start__isnull=True));
        
        customer_pickup_weekly_and_one_time= customer_active_account.filter(Q(one_time_pickup= date_numbers) | Q(weekly_pickup= day_of_week )) 
        
        customer_ready_for_pickup= customer_pickup_weekly_and_one_time.filter(Q(date_of_last_pickup__lt = date_numbers) |Q(date_of_last_pickup__isnull=True))
        
        
        context = {
            'logged_in_employee': logged_in_employee,
            'Customer': Customers,
            'all_customers': all_customers,
            'date_numbers': date_numbers,
            'day_of_week': day_of_week,
            'customer_matching_zip_code': customer_matching_zip_code,            
            'customer_active_account': customer_active_account,
            'customer_ready_for_pickup': customer_ready_for_pickup,
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



def confirm_pickup(request, customer_id): 
    
    
    try:
        Customer = apps.get_model('customers.Customer')   
        customer_to_update = Customer.objects.get(id=customer_id)
        customer_to_update.balance += 20
        customer_to_update.date_of_last_pickup = date.today()
        customer_to_update.save()
        return  HttpResponseRedirect(reverse('employees:index'))
    except ObjectDoesNotExist:        
        return render(request,'employees/index.html')
        



@login_required   
def choose_day(request, picked_day):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)    
#     customer_on_tuesday=  customer_matching_zip_code.filter(weekly_pickup= 'tuesday')
#     customer_on_thursday=  customer_matching_zip_code.filter(weekly_pickup= 'wednesday')
#     customer_on_friday=     customer_matching_zip_code.filter(weekly_pickup= 'friday')
#     customer_on_saturday=   customer_matching_zip_code.filter(weekly_pickup= 'saturday')
    day_of_week= picked_day
    try:
        Customer = apps.get_model('customers.Customer')
        all_customers= Customer.objects.all() 
        customer_matching_zip_code = all_customers.filter(zip_code=logged_in_employee.zip_code)
        customer_on_monday=   customer_matching_zip_code.filter(weekly_pickup= day_of_week)
        context = {
            'logged_in_employee': logged_in_employee,
            'customer_matching_zip_code': customer_matching_zip_code,
            'customer_on_monday': customer_on_monday, 
            'day_of_week': day_of_week
        } 
        return render(request,'employees/choose_day.html',context)
    except ObjectDoesNotExist:     
       
        return  HttpResponseRedirect(reverse('employees:index'))