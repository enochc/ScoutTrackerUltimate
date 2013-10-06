from django.contrib import admin
from django.db import models
from utils.widgets import AdminImageWidget
from applications.award.models import Award, AwardRequirement

class AwardRequirementAdmin(admin.ModelAdmin):
    pass


class AwardAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }
    list_display = ('name','required', 'image')
    list_editable = ('required','image')
    
    
admin.site.register(Award, AwardAdmin)
admin.site.register(AwardRequirement, AwardRequirementAdmin)