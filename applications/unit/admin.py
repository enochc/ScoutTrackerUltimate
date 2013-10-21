from django.contrib import admin

from applications.unit.models import Unit, Patrol, UnitRequest

class AdminUnitRequest(admin.ModelAdmin):
    list_display = ('unit', 'type','key','email')

admin.site.register(Unit)

admin.site.register(Patrol)

admin.site.register(UnitRequest, AdminUnitRequest)