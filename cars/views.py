from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView, TemplateView
from django.conf import settings

from .forms import CarsForm
from .models import Cars
from .usecases import *
from mock.usecases import *

class AddCarView(CreateView):
    modal = Cars
    form_class = CarsForm
    template_name = 'add_car.html'
    success_url = '/cars/'

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            car = form.save(commit=False)
            car.author = self.request.user
            car.save()
        return redirect('cars_view')

class CarsListView(ListView):
    modal = Cars
    template_name = 'cars_view.html'

    def get_queryset(self):
        return Cars.objects.all()
    

class CarDetailsView(DetailView):
    modal = Cars
    template_name = 'car_details.html'

    def get_queryset(self):
        return Cars.objects.filter(id=self.kwargs['pk'])


class CarUpdateView(LoginRequiredMixin,UserPassesTestMixin,  UpdateView):
    modal = Cars
    form_class = CarsForm
    template_name = 'update_car.html'
    success_url = '/cars/'

    def get_queryset(self):
        return Cars.objects.filter(id=self.kwargs['pk'])

    def test_func(self):
        car = self.get_object()
        if self.request.user == car.author:
            return True
        return False


@login_required
def delete_car(request, car_id: int):
    car = Cars.objects.get(id=car_id)
    car.delete()
    messages.success(request, 'Машина удалено успешно!')
    return redirect('cars_view')

@login_required
def add_to_buy(request, car_id: int):
    car = Cars.objects.get(id=car_id)
    added = send_to_buy(request, car_id, 'car')

    if not added:
        messages.success(
            request, f"Машина {car.title.upper()} успешно добавлено в корзинку!")
    else:
        messages.warning(
            request, f"Машина {car.title.upper()} уже существует в вашем корзинке!")
    return redirect('cars_view')
