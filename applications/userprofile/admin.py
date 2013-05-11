from django.contrib import admin

from applications.userprofile.models import Userprofile

class UserprofileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'troop')


admin.site.register(Userprofile, UserprofileAdmin)