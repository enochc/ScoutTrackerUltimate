from django.contrib import admin

from applications.rank.models import Rank

class RankAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', )
    ordering = ('order',)
    list_editable = ('order',)

admin.site.register(Rank, RankAdmin)