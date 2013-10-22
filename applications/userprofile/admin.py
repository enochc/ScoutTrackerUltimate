from django.contrib import admin

from applications.userprofile.models import Userprofile, UserAward

class UserawardAdmin(admin.ModelAdmin):
    list_display = ("user","award")

class UserprofileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'unit', 'google_id', 'facebook_id')
    list_editable = ("facebook_id",)


admin.site.register(Userprofile, UserprofileAdmin)
admin.site.register(UserAward, UserawardAdmin)