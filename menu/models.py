from django.utils import timezone
from django.db import models


class PrimaryMeal(models.Model):
    '''Модель списка фирменных блюд'''
    name = models.CharField(
        verbose_name='Название фирменного блюда',
        max_length=60
    )

    kitchen = models.CharField(
        verbose_name='Страна кухни',
        max_length=50
    )
    
    primary_meal_image = models.ImageField(
        verbose_name='Фото фирменного блюда',
        upload_to='primary_meal_photo'
    )

    ingredients = models.CharField(
        verbose_name='Ингредиенты фирменного блюда',
        max_length=100
    )

    price = models.IntegerField(
        verbose_name= 'Цена фирменного блюда',
    )

    date_created = models.DateTimeField(
        verbose_name='Дата создания записи',
        default=timezone.now
    )

    def __str__(self):
        '''Описание объекта PrimaryMeal'''
        return f'{self.name} {self.kitchen} {self.date_created}'



class Wine(models.Model):
    '''Модель списка вин'''
    name = models.CharField(
        verbose_name='Название Вина',
        max_length=50
    )

    wine_image = models.ImageField(
        verbose_name='Фото Вина',
        upload_to='wine_photo'
    )

    description = models.CharField(
        verbose_name='Описание Вина',
        max_length=150
    )

    category = models.CharField(
        verbose_name='Вид Вина',
        max_length=20
    )

    priority = models.IntegerField(
        verbose_name='Приоритет',

    )

    color = models.CharField(
        verbose_name='Цвет Вина',
        max_length=30
    )

    price = models.IntegerField(
        verbose_name= 'Цена Вина',
    )

    date_created = models.DateTimeField(
        verbose_name='Дата создания записи',
        default=timezone.now
    )

    def __str__(self):
        '''Описание объекта Wine'''
        return f'{self.name} {self.color} {self.date_created}'

class Breackfast(models.Model):
    '''Модель списка завтраков'''
    name = models.CharField(
        verbose_name='Название завтрака',
        max_length=50
    ) 

    breackfast_image = models.ImageField(
        verbose_name='Фото Завтрака',
        upload_to='breackfast_photo'
    )

    price = models.IntegerField(
        verbose_name= 'Цена Завтрака',
    )

    ingredients = models.CharField(
        verbose_name='Ингредиенты блюда',
        max_length=100
    )

    date_to_present = models.DateTimeField(
        verbose_name='Срок годности блюда'
    )

    date_created = models.DateTimeField(
        verbose_name='Дата создания записи',
        default=timezone.now
    )

    def __str__(self):
        '''Описание объекта Breackfast'''
        return f'{self.name} {self.date_created}'

class Lunch(models.Model):
    '''Модель списка обедов'''
    name = models.CharField(
        verbose_name='Название обеда',
        max_length=50
    ) 

    lunch_image = models.ImageField(
        verbose_name='Фото обеда',
        upload_to='lunch_photo'
    )

    price = models.IntegerField(
        verbose_name= 'Цена обеда',
    )

    ingredients = models.CharField(
        verbose_name='Ингредиенты блюда',
        max_length=100
    )

    date_to_present = models.DateTimeField(
        verbose_name='Срок годности блюда'
    )

    date_created = models.DateTimeField(
        verbose_name='Дата создания записи',
        default=timezone.now
    )

    def __str__(self):
        '''Описание объекта Lunch'''
        return f'{self.name} {self.date_created}'

class Dinner(models.Model):
    '''Модель списка ужина'''
    name = models.CharField(
        verbose_name='Название ужина',
        max_length=50
    ) 

    dinner_image = models.ImageField(
        verbose_name='Фото Ужина',
        upload_to='dinner_photo'
    )

    price = models.IntegerField(
        verbose_name= 'Цена Ужина',
    )

    ingredients = models.CharField(
        verbose_name='Ингредиенты блюда',
        max_length=100
    )

    date_to_present = models.DateTimeField(
        verbose_name='Срок годности блюда'
    )

    date_created = models.DateTimeField(
        verbose_name='Дата создания записи',
        default=timezone.now
    )
    
    def __str__(self):
        '''Описание объекта Dinner'''
        return f'{self.name} {self.date_created}'
    

