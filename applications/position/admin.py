from django.contrib import admin
from django.db import models
from utils.widgets import AdminImageWidget

from applications.position.models import Position

class PositionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }
    
    list_display = ('name', 'youth', 'patch')
    list_filter = ('youth',)
    list_editable = ('youth', 'patch')

admin.site.register(Position, PositionAdmin)