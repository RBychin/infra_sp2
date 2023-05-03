from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'description',
        'category',
    )
    list_display_links = (
        'name',
    )
    empty_value_display = '-пусто-'
    list_editable = ('year',)
    search_fields = ('name',)
    list_filter = ('category',)
    filter_horizontal = ('genre',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    list_display_links = (
        'name',
    )
    empty_value_display = '-пусто-'
    list_editable = ('slug',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    list_display_links = (
        'name',
    )
    empty_value_display = '-none-'
    list_editable = ('slug',)
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'score', 'pub_date', 'title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'pub_date', 'review')
