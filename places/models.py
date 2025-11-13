from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Place(models.Model):
    title = models.CharField("Название", max_length=200)
    description_short = models.TextField("Описание")
    description_long = models.TextField("Подробности")
    # image = models.ImageField("Картинка")
    lng = models.FloatField(verbose_name='Долгота')
    lat = models.FloatField(verbose_name='Широта')
    

    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     verbose_name="Автор",
    #     limit_choices_to={'is_staff': True})
    # likes = models.ManyToManyField(
    #     User,
    #     related_name="liked_posts",
    #     verbose_name="Кто лайкнул",
    #     blank=True)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('post_detail', args={'slug': self.slug})

    class Meta:
        ordering = ['title']
        verbose_name = 'place'
        verbose_name_plural = 'places'