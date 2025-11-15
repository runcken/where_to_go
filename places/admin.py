from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase, SortableAdminMixin
from .models import Place, PlaceImage


class PlaceImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    extra = 1
    fields = ['image', 'image_preview', 'order']
    readonly_fields = ['image_preview']

    # def get_queryset(self, request):
    #     return super().get_queryset(request).select_related('place')


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ['title', 'place_id', 'lng', 'lat']
    list_editable = ['place_id']
    search_fields = ['title', 'place_id']
    inlines = [PlaceImageInline]

    # def image_count(self, obj):
    #     return obj.images.count()
    # image_count.short_description = 'Количество фото'


@admin.register(PlaceImage)
class PlaceImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['place', 'image', 'order']
    # list_filter = ['place']
    # readonly_fields = ['admin_thumbnail']

    # def admin_thumbnail(self, obj):
    #     if obj.image:
    #         return format_html(
    #             '<div style="width: 50px; height: 50px; display: flex; align-items: center, justify-content: center;">'
    #             'img src="{}" style="max-width: 100%; max-height: 100%; object-fit; contain;" />'
    #             '</div>',
    #             obj.image.url
    #         )
    #     return "-"

    # admin_thumbnail.short_description = 'Превью'
