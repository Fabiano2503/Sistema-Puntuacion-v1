from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('history/', views.history, name='reports_history'),
    path('history/export/excel/', views.export_history_excel, name='export_history_excel'),
    path('history/export/pdf/', views.export_history_pdf, name='export_history_pdf'),
    path('close-biweekly/', views.close_biweekly, name='close_biweekly'),
]