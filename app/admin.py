from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Publication, Video, VideoSet, RouteImage, PressMention, YearPeriod, ExhibitionImage, ExhibitionPDFImage, RouteVideo, Artist, Artwork, ArtworkImage, ArtistVideo, Exhibition, Employee, PostalLink, FlowEvent, Route, PageArtwork, YearPeriodArtwork, RouteArtwork
)
from django.db import models
from django import forms
from modeltranslation.admin import TranslationAdmin
from unfold.admin import ModelAdmin, StackedInline
from unfold.contrib.forms.widgets import WysiwygWidget
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin, SortableAdminBase

from django.utils.safestring import mark_safe


class ArtworkImageInline(admin.TabularInline):
    model = ArtworkImage
    extra = 0
    readonly_fields = ("preview", )
    show_change_link = True

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "Нет изображения"

    preview.short_description = "Превью"
class ExhibitionImageImageInline(admin.TabularInline):
    model = ExhibitionImage
    extra = 0
    readonly_fields = ("preview", 'uploaded_at')

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "Нет изображения"

    preview.short_description = "Превью"
class ExhibitionPDFImageeInline(admin.TabularInline):
    model = ExhibitionPDFImage
    extra = 0
    readonly_fields = ("preview", )
    show_change_link = True

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "Нет изображения"

    preview.short_description = "Превью"
class VideoInline(admin.TabularInline):
    model = Video
    extra = 0
    readonly_fields = ("preview",)
    show_change_link = True

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "Нет изображения"

    preview.short_description = "Превью"

# class ArtworkInline(SortableInlineAdminMixin, admin.StackedInline):
#     model = Artwork
#     extra = 0
#     fields = ['preview', 'order_desktop', 'order_mobile']
#     readonly_fields = ['preview']
#     show_change_link = True
#     ordering_field = "order_mobile"
#     hide_ordering_field = True

#     def get_ordering(self, request):
#         mode = request.GET.get('mode', 'desktop')
#         return ['order_mobile'] if mode == 'mobile' else ['order_desktop']

#     class Media:
#         js = ('admin/js/artwork_order_toggle.js',)

    

#     def preview(self, obj):
#         if obj.main_image:
#             return format_html('''
#                 <div style="
#                     display: flex;
#                     flex-direction: column;
#                     align-items: center;
#                     gap: 8px;
#                     padding: 12px;

#                     border-radius: 12px;
#                     box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
#                 ">
#                     <img src="{}" style="
#                         max-width: 100%;
#                         max-height: 120px;
#                         object-fit: contain;
#                         border-radius: 8px;
#                         box-shadow: 0 1px 3px rgba(0,0,0,0.08);
#                     " />
#                 </div>
#             ''', obj.main_image.url)
#         return format_html('<div style="padding: 12px; border: 1px dashed #ddd; border-radius: 12px; text-align: center;">Нет изображения</div>')

#     preview.short_description = "Превью"

class ArtworkRelationInline(SortableInlineAdminMixin, admin.TabularInline):
    """
    Абстрактный базовый Inline для связи Artwork с чем-либо.
    """
    extra = 0
    fields = ['artwork', 'order_desktop', 'order_mobile']
    autocomplete_fields = ['artwork']

    class Media:
        js = ('admin/js/artwork_order_toggle.js',)

    def get_ordering(self, request):
        mode = request.GET.get('mode', 'desktop')
        return ['order_mobile'] if mode == 'mobile' else ['order_desktop']
    
class PageArtworkInline(ArtworkRelationInline):
    model = PageArtwork

class YearPeriodArtworkInline(ArtworkRelationInline):
    model = YearPeriodArtwork

class RouteArtworkInline(ArtworkRelationInline):
    model = RouteArtwork


class RouteImageImageInline(admin.TabularInline):
    model = RouteImage
    extra = 0
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "Нет изображения"

    preview.short_description = "Превью"

# class ArtistPDFInline(admin.TabularInline):
#     model = ArtistPDF
#     extra = 0  # Количество пустых полей для добавления новых произведений
#     fields = ['title', 'file']
#     readonly_fields = ['is_visible']

class ArtistVideoInline(admin.TabularInline):
    model = ArtistVideo
    extra = 0
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "Нет изображения"

    preview.short_description = "Превью"

class RouteVideoInline(admin.TabularInline):
    model = RouteVideo
    extra = 0  # Количество пустых полей для добавления новых произведений
    fields = ['image',]
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "Нет изображения"

    preview.short_description = "Превью"

@admin.register(Artist)
class ArtistAdmin(SortableAdminBase, TranslationAdmin, ModelAdmin):
    list_display = ['name', 'is_visible', 'birth_year']
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['birth_year', 'death_year']
    # inlines = [ArtworkInline, ArtistVideoInline]
    inlines = [ArtistVideoInline]

    fieldsets = [
        (None,
        {
            "fields": ["is_visible", "photo", "created_at", "updated_at"],
        },
        ),
        ("💠 Имя",
            {
                "classes": ["collapse in"],
                "fields": ["name"],
            },
        ),
        ("💠 Информация",
            {
                "classes": ["collapse"],
                "fields": ["birth_year", "death_year", "photoAuthor", "textAuthor"],
            },
        ),
        ("💠 Описание",
            {
                "classes": ["collapse"],
                "fields": ["description"],
            },
        ),
        ("💠 Видео",
            {
                "classes": ["collapse"],
                "fields": ["video_name", "video_link", "video_preview"],
            },
        ),
    ]

    formfield_overrides = {
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
    list_display = ['preview_image', 'title', 'is_visible', 'artist']
    search_fields = ['title', 'artist__name']
    list_filter = ['artist']
    inlines = [ArtworkImageInline]

    formfield_overrides = {
        # models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'style': 'height: 40px;'})}, 
        models.TextField: {
            "widget": WysiwygWidget,
        } 
    }

    def preview_image(self, obj):
        if obj.main_image:
            return format_html('''
                <div style="
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 8px;
                    padding: 12px;
                    width: 100px;
                    height: 100px;
                    background: #fff;
                    border-radius: 12px;
                    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
                ">
                    <img src="{}" style="
                        width: 100%;
                        height: 100%;  
                        object-fit: contain;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                    " />
                </div>
            ''', obj.main_image.url)
        return format_html('<div style="padding: 12px; border: 1px dashed #ddd; border-radius: 12px; text-align: center;">Нет изображения</div>')

    preview_image.short_description = 'Фото'

@admin.register(PressMention)
class PressMentionAdmin(TranslationAdmin, ModelAdmin):
    list_display = ['title', 'is_visible']
    search_fields = ['title']

@admin.register(Publication)
class PublicationAdmin(TranslationAdmin, ModelAdmin):
    list_display = ['title', 'is_visible']
    search_fields = ['title']

@admin.register(Exhibition)
class ExhibitionAdmin(SortableAdminBase, TranslationAdmin, ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'location']
    search_fields = ['title', 'location']
    list_filter = ['start_date', 'end_date']
    # filter_horizontal = ['artworks']
    inlines = [PageArtworkInline, ExhibitionPDFImageeInline, ExhibitionImageImageInline]
    exclude = ('artworks',)
    fieldsets = [
        (None,
            {
                "fields": ["is_visible", "is_own", "start_date", "end_date", "image"],
            },
        ),
        ("💠 Название",
            {
                "classes": ["collapse in"],
                "fields": ["title"],
            },
        ),
        ("💠 Описание",
            {
                "classes": ["collapse"],
                "fields": ["text"],
            },
        ),
        (
            "💠 Информация",
            {
                "classes": ["collapse"],
                "fields": ["location", "curators"],
            },
        ),
                (
            "💠 Файлы",
            {
                "classes": ["collapse"],
                "fields": ["press_kit_zip", "catalog_pdf"],
            },
        ),
    ]
    

    formfield_overrides = {
        # models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'style': 'height: 40px;'})}, 
        models.TextField: {
            "widget": WysiwygWidget,
        } 
    }

@admin.register(YearPeriod)
class YearPeriodAdmin(SortableAdminBase, TranslationAdmin, ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    # filter_horizontal = ['artworks']

    inlines = [YearPeriodArtworkInline]
    exclude = ('artworks',)

    formfield_overrides = {
        # models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'style': 'height: 40px;'})}, 
        models.TextField: {
            "widget": WysiwygWidget,
        } 
    }

@admin.register(Employee)
class EmployeeAdmin(SortableAdminMixin, TranslationAdmin, ModelAdmin):
    list_display = ['name', 'position', 'order']
    readonly_fields = ['preview_image']
    ordering = ['order'] 

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
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
    list_display = ['text', 'preview_image']
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

@admin.register(VideoSet)
class VideoSetAdmin(TranslationAdmin, ModelAdmin):
    list_display = ['title', 'color_display']
    inlines = [VideoInline]

    def color_display(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color:{}; border: 1px solid #000;"></div>',
            obj.color
        )

    color_display.short_description = "Цвет"

@admin.register(Route)
class RouteAdmin(SortableAdminBase, TranslationAdmin, ModelAdmin):
    list_display = ['title', 'color_display']
    # filter_horizontal = ['artworks']
    inlines = [RouteArtworkInline, RouteImageImageInline, RouteVideoInline]
    exclude = ('artworks',)

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

    fieldsets = [
        (None,
        {
            "fields": ["image", "color", "route_video"]
        },
        ),
        ("💠 Название",
            {
                "classes": ["collapse in"],
                "fields": ["title"],
            },
        ),
        ("💠 Описание",
            {
                "classes": ["collapse"],
                "fields": ["short_description", "full_description"],
            },
        ),
        ("💠 Статья",
            {
                "classes": ["collapse"],
                "fields": ["article_title", "article_author", "article"],
            },
        ),
    ]

    
