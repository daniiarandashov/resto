from django import forms
from django.forms import fields
from .models import Order

class ReservationForm(forms.ModelForm):
    '''Форма создания Брони.Унаследовал от модели Order'''
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['reservator', 'date_created']
    