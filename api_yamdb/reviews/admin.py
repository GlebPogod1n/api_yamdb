from django.contrib import admin

from .models import Comment, Review, Genre, Category, Title


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'score',
        'pub_date',
        'author',
        'title'
    )
    search_fields = ('text', 'pub_date', 'author', 'score')
    list_filter = ('pub_date', 'score')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'author',
        'text',
        'pub_date'
    )
    list_display_links = ('text',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_editable = ('name', 'slug')
    search_fields = ('name', 'slug')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_editable = ('name', 'slug')
    search_fields = ('name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'description',
        'category',
    )
    list_editable = ('name', 'description', 'category', 'year')
    search_fields = ('name', 'year', 'genre', 'category')


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
