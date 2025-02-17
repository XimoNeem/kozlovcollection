from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ExhibitionPDFImage, RouteVideo, Artist, Artwork, ArtworkImage, ArtistVideo, ArtistPDF, Exhibition, Employee, PostalLink, FlowEvent, Route, 
)
from django.db import models
from django import forms
from modeltranslation.admin import TranslationAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget



class ArtworkImageInline(admin.TabularInline):
    model = ArtworkImage
    extra = 0
    readonly_fields = ("preview", 'uploaded_at')
    show_change_link = True

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "Нет изображения"

    preview.short_description = "Превью"

class ExhibitionPDFImageeInline(admin.TabularInline):
    model = ExhibitionPDFImage
    extra = 0
    readonly_fields = ("preview", 'uploaded_at')
    show_change_link = True

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "Нет изображения"

    preview.short_description = "Превью"

class ArtworkInline(admin.TabularInline):  # Можно заменить на admin.StackedInline
    model = Artwork
    extra = 0  # Количество пустых полей для добавления новых произведений
    fields = ['title']
    readonly_fields = ['is_visible']
    #readonly_fields = ['preview_images']  # Предпросмотр изображений
    show_change_link = True  # Добавляет ссылку на редактирование объекта

    def preview_images(self, obj):
        return obj.preview_images() if obj else "Нет изображений"
    
    preview_images.short_description = "Превью"

class ArtistPDFInline(admin.TabularInline):
    model = ArtistPDF
    extra = 0  # Количество пустых полей для добавления новых произведений
    fields = ['title', 'file']
    readonly_fields = ['is_visible']

class ArtistVideoInline(admin.TabularInline):
    model = ArtistVideo
    extra = 0  # Количество пустых полей для добавления новых произведений
    fields = ['title', 'url']
    readonly_fields = ['is_visible']

class RouteVideoInline(admin.TabularInline):
    model = RouteVideo
    extra = 0  # Количество пустых полей для добавления новых произведений
    fields = ['title', 'url', 'image']

@admin.register(Artist)
class ArtistAdmin(TranslationAdmin, ModelAdmin):
    list_display = ['name', 'is_visible', 'birth_year']
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['birth_year', 'death_year']
    inlines = [ArtworkInline, ArtistPDFInline, ArtistVideoInline]  # Добавляем Inline для работ художника

    formfield_overrides = {
        # models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'style': 'height: 40px;'})}, 
        models.TextField: {
            "widget": WysiwygWidget,
        } 
    }

    def preview_image(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.photo.url)
        return "Нет изображения"

    preview_image.short_description = 'Фото'


@admin.register(Artwork)
class ArtworkAdmin(TranslationAdmin, ModelAdmin):
    list_display = ['title', 'is_visible', 'artist']
    search_fields = ['title', 'artist__name']
    list_filter = ['artist']
    inlines = [ArtworkImageInline]

    formfield_overrides = {
        # models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'style': 'height: 40px;'})}, 
        models.TextField: {
            "widget": WysiwygWidget,
        } 
    }


@admin.register(Exhibition)
class ExhibitionAdmin(TranslationAdmin, ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'location']
    search_fields = ['title', 'location']
    list_filter = ['start_date', 'end_date']
    filter_horizontal = ['artworks']
    inlines = [ExhibitionPDFImageeInline]

    formfield_overrides = {
        # models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'style': 'height: 40px;'})}, 
        models.TextField: {
            "widget": WysiwygWidget,
        } 
    }


@admin.register(Employee)
class EmployeeAdmin(TranslationAdmin, ModelAdmin):
    list_display = ['name', 'position']
    readonly_fields = ['preview_image']

    formfield_overrides = {
        # models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'style': 'height: 40px;'})}, 
        models.TextField: {
            "widget": WysiwygWidget,
        } 
    }

    def preview_image(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.photo.url)
        return "Нет изображения"

    preview_image.short_description = 'Фото'


@admin.register(PostalLink)
class PostalLinkAdmin(TranslationAdmin, ModelAdmin):
    list_display = ['title', 'email']
    search_fields = ['title', 'email']

    formfield_overrides = {
        # models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'style': 'height: 40px;'})}, 
        models.TextField: {
            "widget": WysiwygWidget,
        } 
    }


@admin.register(FlowEvent)
class FlowEventAdmin(TranslationAdmin, ModelAdmin):
    list_display = ['id', 'preview_image']
    readonly_fields = ['preview_image']

    formfield_overrides = {
        # models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'style': 'height: 40px;'})}, 
        models.TextField: {
            "widget": WysiwygWidget,
        } 
    }

    def preview_image(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.photo.url)
        return "Нет изображения"

    preview_image.short_description = 'Фото'


@admin.register(Route)
class RouteAdmin(TranslationAdmin, ModelAdmin):
    list_display = ['title', 'color_display']
    filter_horizontal = ['artworks']
    #inlines = [RouteVideoInline]

    formfield_overrides = {
        # models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'style': 'height: 40px;'})}, 
        models.TextField: {
            "widget": WysiwygWidget,
        } 
    }

    def color_display(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color:{}; border: 1px solid #000;"></div>',
            obj.color
        )

    color_display.short_description = "Цвет"
