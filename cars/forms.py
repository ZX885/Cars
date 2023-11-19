from django import forms
from django.contrib.auth.models import User
from .models import Cars

type_choices = (
    ("Sport car", "Sedan"),
    ("Racing", "Truck"),
    ("Drift", "German cars"),
    ("American cars", "Japanese cars"),
    ("Italian cars", "Uzb cars"),
    ("formula", "fast"),
    ("Bus", "electric"),
)

class CarsForm(forms.ModelForm):
    name = forms.CharField(max_length=255, label="Car name",
                            help_text="How your car will be called")
    type = forms.CharField(max_length=255, label="Type", help_text="Enter main type of your car",
                            widget=forms.Select(choices=type_choices))
    price = forms.DecimalField(max_digits=5, decimal_places=2, label="Price",
                               help_text="Please enter price")
    image = forms.ImageField(required=False, label="Car image",
                             help_text="Please upload car image")
    description = forms.CharField(max_length=255, label="Description", help_text="Please enter description",
                                  widget=forms.Textarea(attrs={'rows': 3, 'cols': 50}))

    class Meta:
        model = Cars
        fields = ['name', 'type', 'price','image','description']
        