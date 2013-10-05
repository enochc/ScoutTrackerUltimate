from django.contrib import admin
from django.db import models
from utils.widgets import AdminImageWidget
from applications.meritbadge.models import Badge, BadgeRequirement

class BadgeRequirementAdmine(admin.ModelAdmin):
    pass


class BadgeAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }
    list_display = ('name','required', 'image')
    list_editable = ('required','image')
    
    
admin.site.register(Badge, BadgeAdmin)
admin.site.register(BadgeRequirement, BadgeRequirementAdmine)