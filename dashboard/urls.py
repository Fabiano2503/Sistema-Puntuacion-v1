from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('export/excel/', views.export_ranking_excel, name='export_ranking_excel'),
    path('export/pdf/', views.export_ranking_pdf, name='export_ranking_pdf'),
]