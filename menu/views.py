from django.shortcuts import render
from .models import PrimaryMeal,Wine,Breackfast,Lunch,Dinner
from django.views.generic import ListView



class PrimaryMealListView(ListView):
    model = PrimaryMeal
    context_object_name = 'meals'
    template_name = 'menu/primary_meals.html'

    def get_context_data(self, **kwargs):
        kwargs["breakfast"] = Breackfast.objects.all()
        kwargs["lunch"] = Lunch.objects.all()
        kwargs["dinner"] = Dinner.objects.all()
        return super().get_context_data(**kwargs)

class WineListView(ListView):
    model = Wine
    context_object_name = 'wines'
    template_name = 'menu/wines.html'

    def get_context_data(self, **kwargs):
        kwargs["wines_first_priority"] = Wine.objects.filter(priority__range = [1,2])
        kwargs["wines_other_priority"] = Wine.objects.filter(priority__range = [3,10])
        return super().get_context_data(**kwargs)

