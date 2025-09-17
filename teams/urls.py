from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.team_management, name='team_management'),
    path('add/', views.add_team, name='add_team'),
    path('edit/<int:team_id>/', views.edit_team, name='edit_team'),
    path('delete/<int:team_id>/', views.delete_team, name='delete_team'),
]