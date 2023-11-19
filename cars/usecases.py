from mock.usecases import *

from .models import Cars
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated


class NoAuthApiView(APIView):
    """Doesn't require authentication"""
    permission_classes = [AllowAny]

class AuthApiView(NoAuthApiView):
    """Requires authentication"""
    permission_classes = [IsAuthenticated]



def get_saved_cars(request) -> list[Cars]:
    cars_ids = getItemsFromWishlist(request, "car")
    cars = []
    for car_ids in cars_ids:
        if car := Cars.objects.filter(id=car_ids).first():
            cars.append(car)
    return cars


def delete_car_from_wl(request, car_ids: int):
    delete_item_from_wishlist(request, car_ids, "car")
