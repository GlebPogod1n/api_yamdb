from django.contrib import admin

from .models import Comment, Review


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


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
