from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.create, name='create'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('<int:customer_id>/', views.confirm_pickup, name= 'confirm_pickup'),
    path('choose_day/<str:picked_day>', views.choose_day, name = 'choose_day')
]