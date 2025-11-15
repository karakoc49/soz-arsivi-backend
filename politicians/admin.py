from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Politician, PoliticianPartyMembership

class PoliticianPartyMembershipInline(admin.TabularInline):
    model = PoliticianPartyMembership
    extra = 1
    autocomplete_fields = ['party']
    fields = ('party', 'start_date', 'end_date')

@admin.register(Politician)
class PoliticianAdmin(ImportExportModelAdmin):
    list_display = ('full_name', 'title', 'active')
    search_fields = ('full_name',)
    list_filter = ('active', 'title')
    inlines = [PoliticianPartyMembershipInline]
