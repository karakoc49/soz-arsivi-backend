from django.contrib import admin
from .models import Party

@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'color_code')
    search_fields = ('name', 'abbreviation')
