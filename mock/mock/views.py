import re
from cars.models import *
from cars.usecases import *
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from smtplib import SMTPException
from django.conf import settings

from .usecases import * 

class HomeView(TemplateView):
    template_name = 'cars.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cars_ids = []
        if wish_list := Session(self.request).get(WISH_LIST, []):
            cars_ids = wish_list.get("car_ids", [])

        context.update({
            "cars_ids": cars_ids
        })
        return context
class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cars_ids = []
        context.update({
            "cars_ids": cars_ids
        })
        # Do something
        return context

def wishlist_view(request):
    context = {
        "cars": get_saved_cars(request),
        
    }
    return render(request, 'wishlist.html', context)


def delete_from_wl(request, car_id: int):
    car = Cars.objects.filter(id=car_id).first()
    delete_car_from_wl(request, car_id)

    messages.success(
        request, f"Successfully deleted {car.title} from wishlist")
    return redirect('wishlist_view')
