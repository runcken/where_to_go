from django.contrib import admin
from .models import Place, PlaceImage


# class PlaceImageInline(admin.TabularInline):
#     model = PlaceImage
#     extra = 1


admin.site.register(Place)
admin.site.register(PlaceImage)
