from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.models import User


class Place(models.Model):
    title = models.CharField('Название', max_length=200)
    description_short = models.TextField('Краткое описание')
    description_long = models.TextField('Полное описание')
    lng = models.FloatField(verbose_name='Долгота')
    lat = models.FloatField(verbose_name='Широта')
    place_id = models.SlugField(
        'Уникальный идентификатор',
        max_length=100,
        unique=True,
        help_text='Латинские буквы, цифры и подчеркивания',
        null=True
    )
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("place_details", args=[self.place_id])

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
        # upload_to='media',
        verbose_name='Изображение'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Позиция'
        )

    class Meta:
        ordering = ['-order']
        verbose_name = 'фотография'
        verbose_name_plural = 'фотографии'

    def __str__(self):
        return f'{self.order} {self.place.title}'

    def image_preview(self):
        if self.image:
            return format_html(
                '<img src="{}" height="200" style="object-fit: contain;" />',
                self.image.url
            )
        return 'Нет изображения'

    image_preview.short_description = 'Превью'