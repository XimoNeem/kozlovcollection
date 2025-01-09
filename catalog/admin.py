from django.contrib import admin
from .models import Author, Work

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ('title', 'author__name')