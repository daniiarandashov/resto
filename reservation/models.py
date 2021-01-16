from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Order(models.Model):
    '''Модель Бронирования имеет 7 полей.'''
    PERSONS = (
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
        ('6', 6)
    )

    reservator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользоватеь'
    )

    phone = models.IntegerField(
        verbose_name='Номер телефона',
    )

    date = models.DateField(
        verbose_name='Дата бронирования'
    )

    time = models.TimeField(
        verbose_name='Время бронирования'
    )

    persons = models.CharField(
        verbose_name='Количество человек',
        choices=PERSONS,
        default=PERSONS[0][1],
        max_length=1
    )

    massage = models.TextField(
        verbose_name='Комментарии',
        max_length=500,
        blank=True,
        default='Коментариев нет'
    )

    date_created = models.DateTimeField(
        verbose_name='Дата создания брони',
        default=timezone.now
    )

    def __str__(self):
        '''Описание объекта Order'''
        return f'{self.reservator} {self.date} {self.time}'
