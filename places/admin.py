from adminsortable2.admin import (
    SortableInlineAdminMixin,
    SortableAdminBase,
    SortableAdminMixin
)
from django.contrib import admin
from tinymce.widgets import TinyMCE

from .models import Place, PlaceImage


class PlaceImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    extra = 1
    fields = ['image', 'image_preview', 'order']
    readonly_fields = ['image_preview']


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ['title', 'lng', 'lat']
    search_fields = ['title']
    inlines = [PlaceImageInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'short_description')
        }),
        ('Геоданные', {
            'fields': ('lng', 'lat'),
            'classes': ('collapse',)
        }),
        ('Полное описание', {
            'fields': ('long_description',),
            'description': 'Используйте редактор для форматирования текста'
            }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'long_description':
            kwargs['widget'] = TinyMCE(attrs={'cols': 80, 'rows': 30})
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(PlaceImage)
class PlaceImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['place', 'image', 'order']
    raw_id_fields = ['place']
