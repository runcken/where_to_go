from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import(
    SortableInlineAdminMixin,
    SortableAdminBase,
    SortableAdminMixin
)
from tinymce.widgets import TinyMCE
from django import forms
from .models import Place, PlaceImage


class PlaceImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    extra = 1
    fields = ['image', 'image_preview', 'order']
    readonly_fields = ['image_preview']


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ['title', 'place_id', 'lng', 'lat']
    list_editable = ['place_id']
    search_fields = ['title', 'place_id']
    inlines = [PlaceImageInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'place_id', 'description_short')
        }),
        ('Геоданные', {
            'fields': ('lng', 'lat'),
            'classes': ('collapse',)
        }),
        ('Полное описание', {
            'fields': ('description_long',),
            'description': 'Используйте редактор для форматирования текста'
            }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'description_long':
            kwargs['widget'] = TinyMCE(attrs={'cols': 80, 'rows': 30})
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(PlaceImage)
class PlaceImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['place', 'image', 'order']
