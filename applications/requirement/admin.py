from django.contrib import admin

from applications.requirement.models import Requirement

class RequirementAdmin(admin.ModelAdmin):
    list_display = ('rank', 'order', 'short_desc', 'type', 'is_last')
    list_filter = ('rank', 'type')
    ordering = ('rank', 'order')
    list_editable = ('order','is_last')

admin.site.register(Requirement, RequirementAdmin)