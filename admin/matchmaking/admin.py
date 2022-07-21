from django.contrib import admin
from .models import EventGroup


# Register your models here.
class EventGroupAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "event",
        "group_no",
    )
    list_filter = (
        "user",
        "event",
    )
    search_fields = ("user", "event")


admin.site.register(EventGroup, EventGroupAdmin)
