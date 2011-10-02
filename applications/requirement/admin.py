from django.contrib import admin

from applications.requirement.models import Requirement

class RequirementAdmin(admin.ModelAdmin):
    list_display = ('rank', 'order', 'short_desc', 'type')
    list_filter = ('rank', 'type')
    ordering = ('rank', 'order')
    list_editable = ('order',)

admin.site.register(Requirement, RequirementAdmin)