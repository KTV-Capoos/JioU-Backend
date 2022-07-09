from django.contrib import admin
from typing import Optional

from .models import Event


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    date_hierarchy: Optional[str] = 'event_date'
    list_display = (
        'event_name',
        'event_date',
        'event_time',
        'event_duration',
        'event_location'
    )


admin.site.register(Event, EventAdmin)
