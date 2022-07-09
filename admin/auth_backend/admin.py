from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserInfo

# Register your models here.
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(UserInfo, UserInfoAdmin)