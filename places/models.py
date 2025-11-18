from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField('Название', max_length=200, unique=True)
    short_description = models.TextField('Краткое описание', blank=True)
    long_description = HTMLField('Полное описание', blank=True)
    lng = models.FloatField(verbose_name='Долгота')
    lat = models.FloatField(verbose_name='Широта')

    class Meta:
        ordering = ['title']
        verbose_name = 'место'
        verbose_name_plural = 'места'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('place_details', args=[self.id])


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Место'
    )
    image = models.ImageField(
        verbose_name='Изображение'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Позиция'
        )

    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['place', 'order']),
            models.Index(fields=['order'], name='order_idx'),
        ]
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
