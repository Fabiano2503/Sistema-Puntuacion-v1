from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    path('add/', views.add_activity, name='add_activity'),
    path('list/', views.activity_list, name='activity_list'),
]