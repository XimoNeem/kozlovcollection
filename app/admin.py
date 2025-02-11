from django.contrib import admin
from .models import Artist, Artwork, PressMention, Route, Translation
from django.utils.html import format_html
from django.contrib.admin import AdminSite


class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_year', 'death_year', 'preview_image', 'created_at', 'updated_at']
    readonly_fields = ['preview_image']
    search_fields = ['name']
    list_filter = ['birth_year', 'death_year']

    def preview_image(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.photo.url)
        return "Нет изображения"
    preview_image.short_description = 'Фото'


class ArtworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'year', 'preview_images', 'created_at', 'updated_at']
    readonly_fields = ['preview_images']
    search_fields = ['title', 'artist__name']
    list_filter = ['year']

    def preview_images(self, obj):
        if obj.images and isinstance(obj.images, list) and len(obj.images) > 0:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.images[0])
        return "Нет изображений"
    preview_images.short_description = 'Изображение'


class PressMentionAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'preview_image', 'created_at', 'updated_at']
    readonly_fields = ['preview_image']
    search_fields = ['title']

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "Нет изображения"
    preview_image.short_description = 'Фото'


class RouteAdmin(admin.ModelAdmin):
    list_display = ("name", "preview_image", "color_display")
    filter_horizontal = ("artworks",)

    def color_display(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color:{}; border: 1px solid #000;"></div>',
            obj.color
        )

    color_display.short_description = "Цвет"


class TranslationInline(admin.TabularInline):
    model = Translation
    extra = 1

# Кастомизация стилей
class MyAdminSite(AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context['admin_css'] = 'admin/css/admin.css'  # Укажите правильный путь
        return context

admin_site = MyAdminSite(name='myadmin')
admin.site = admin_site

# Регистрация моделей
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(PressMention, PressMentionAdmin)
admin.site.register(Route, RouteAdmin)

