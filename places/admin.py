from django.contrib import admin
from .models import Place, PlaceImage


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    extra = 1


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'place_id', 'lng', 'lat']
    list_editable = ['place_id']
    search_fields = ['title', 'place_id']
    inlines = [PlaceImageInline]


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ['place', 'image', 'order']
    list_editable = ['order']
    list_filter = ['place']
