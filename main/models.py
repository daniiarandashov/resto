from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse


class UserProfile(models.Model):
    '''Модель профиля пользователя'''
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    user_photo = models.ImageField(
        upload_to='user_profiles'
    )

    def __str__(self):
        return self.user.username + ' Profile'

class Feedback(models.Model):
    '''Данная модель создает объект Отзывы в базе данных'''
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва'
    )

    feedback_text = models.TextField(
        verbose_name='Оставте отзыв',
        max_length=255

    )

    date_created = models.DateTimeField(
        verbose_name='Дата создания отзыва',
        default=timezone.now

    )
    def get_absolute_url(self):
        return reverse('feedbacks')

    def __str__(self):
        '''Описание объекта Feedback'''
        return f'{self.author.first_name} {self.author.last_name} {self.date_created}'

class Comment(models.Model):
    author = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments'
    )
    author_2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор Отзыва'
    )

    comment_text = models.CharField(
        verbose_name='Содержание отзыва',
        max_length=255
    )
    date_created = models.DateTimeField(
        verbose_name='Дата создания отзыва',
        default=timezone.now

    )
    def __str__(self):
        '''Описание объекта Comment'''
        return f'{self.author_2.first_name} {self.author_2.last_name} {self.date_created}'




