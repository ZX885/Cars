from django.urls import path

from .views import *


urlpatterns = [
    path("", CarsListView.as_view(), name="cars_view"),
    path("add_car", AddCarView.as_view(), name="add_car"),
    path("update_car/<int:pk>", CarUpdateView.as_view(), name="update_car"),
    path("car_details/<int:pk>", CarDetailsView.as_view(), name="car_details"),
    path("delete_car/<int:car_id>", delete_car, name="delete_car"),
    path("add_to_buy/<int:car_id>", 
         add_to_buy, name="purchase"),
]
