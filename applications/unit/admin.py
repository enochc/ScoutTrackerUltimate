from django.contrib import admin

from applications.unit.models import Unit, Patrol, UnitRequest

admin.site.register(Unit)

admin.site.register(Patrol)

admin.site.register(UnitRequest)