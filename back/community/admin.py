from django.contrib import admin
from .models import Discussion

@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'movie', 'content', 'created_at')
    list_filter = ('created_at', 'movie', 'user')
    search_fields = ('content', 'user__username', 'movie__title')
    ordering = ('-created_at',)