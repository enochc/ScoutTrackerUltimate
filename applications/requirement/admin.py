from django.contrib import admin

from applications.requirement.models import Requirement

class RequirementAdmin(admin.ModelAdmin):
    
    list_filter = ('rank',)

admin.site.register(Requirement, RequirementAdmin)