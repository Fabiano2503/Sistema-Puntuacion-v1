from django.contrib import admin
from .models.activity import Activity
from .models.activity_type import ActivityType

@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'points')
    search_fields = ('name',)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_type', 'user', 'date', 'evidence')
    list_filter = ('activity_type', 'date')
    search_fields = ('user__name', 'activity_type__name')