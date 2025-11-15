from django.contrib import admin
from .models import Topic, StatementTopic

class StatementTopicInline(admin.TabularInline):
    model = StatementTopic
    extra = 1
    autocomplete_fields = ['topic']

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(StatementTopic)
class StatementTopicAdmin(admin.ModelAdmin):
    list_display = ('statement', 'topic')
    autocomplete_fields = ['statement', 'topic']
