from django.contrib import admin
from django.utils.html import format_html

from .models import Statement

@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = ('politician', 'statement_type', 'published_at', 'source')
    search_fields = ('content', 'source')
    list_filter = ('statement_type', 'published_at')
    date_hierarchy = 'published_at'
    autocomplete_fields = ['politician']

    def media_preview(self, obj):
        if obj.statement_type == 'image' and obj.media_file:
            return format_html('<img src="{}" style="height: 100px;" />', obj.media_file.url)
        elif obj.statement_type == 'video' and obj.media_file:
            return format_html('<video width="160" height="90" controls><source src="{}" type="video/mp4"></video>',
                               obj.media_file.url)
        return "No media"

    media_preview.short_description = 'Media Preview'
