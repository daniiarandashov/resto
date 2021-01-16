from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

class Cook(models.Model):
    POSITION = (
        ('Генеральный Директор', 'Генеральный Директор'),
        ('Шеф Повар','Шеф Повар'),
        ('Повар','Повар'),
        ('Стажёр', 'Стажер'),
    )
    EDUCATION = (
        ('Бакалавр','Бакалавр'),
        ('Техникум и Колледж','Техникум и Колледж'),
        ('Самоучка','Самоучка')
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    
    position = models.CharField(
        verbose_name='Позиция',
        choices=POSITION,
        default=POSITION[0][1],
        max_length=30
    )
    education = models.CharField(
        verbose_name='Образование',
        choices=EDUCATION,
        default=EDUCATION[0][1],
        max_length=30
    )
    experience = models.IntegerField(
        verbose_name='Реальный стаж работы'
    )
    history_of_work = models.CharField(
        verbose_name='История Работы',
        max_length=100
    )
    def get_absolute_url(self):
        return reverse('teams:teams', kwargs={'pk':self.pk})


    def __str__(self):
        return f'{self.user} {self.position}'



