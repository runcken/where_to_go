from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Place(models.Model):
    title = models.CharField("Название", max_length=200)
    description_short = models.TextField("Описание")
    description_long = models.TextField("Подробности")
    lng = models.FloatField(verbose_name='Долгота')
    lat = models.FloatField(verbose_name='Широта')
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'место'
        verbose_name_plural = 'места'


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='media',
        verbose_name='Изображение'
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-order']

    def __str__(self):
        return f'{self.order} {self.place.title}'
