from django.contrib import admin
from .models.period import Period
from .models.ranking import Ranking

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('type', 'startDate', 'endDate', 'is_closed')
    list_filter = ('type', 'is_closed')

@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    list_display = ('user', 'period', 'position', 'total_points', 'total_activities')
    list_filter = ('period',)
    search_fields = ('user__name',)