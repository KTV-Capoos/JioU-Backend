from django.contrib import admin

from .models import Attendance


# Register your models here.
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'event')
    list_filter = ('user', 'event')
    search_fields = ('user', 'event')
    ordering = ('user', 'event')


admin.site.register(Attendance, AttendanceAdmin)
