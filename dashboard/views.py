from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from activities.models import Activity
from users.models.user import User

@login_required
def dashboard(request):
    # Obtener el período seleccionado (diario, semanal, quincenal)
    period = request.GET.get('period', 'diario')
    
    # Calcular fechas según el período
    today = timezone.now().date()
    if period == 'diario':
        start_date = today
    elif period == 'semanal':
        start_date = today - timedelta(days=today.weekday())
    else:  # quincenal
        start_date = today - timedelta(days=14)
    
    # Obtener actividades del período
    activities = Activity.objects.filter(date__gte=start_date)
    
    # Calcular puntos por usuario
    user_points = {}
    user_activities_count = {}
    
    for activity in activities:
        user_id = activity.user.id
        if user_id not in user_points:
            user_points[user_id] = {
                'user': activity.user,
                'total': 0,
                'activities_count': 0,
                'by_type': {}
            }
        
        user_points[user_id]['total'] += activity.activity_type.points
        user_points[user_id]['activities_count'] += 1
        
        # Contar por tipo de actividad
        activity_type_name = activity.activity_type.name.lower()
        if activity_type_name not in user_points[user_id]['by_type']:
            user_points[user_id]['by_type'][activity_type_name] = 0
        user_points[user_id]['by_type'][activity_type_name] += activity.activity_type.points
    
    # Convertir a lista y ordenar por puntos totales
    ranking = sorted(user_points.values(), key=lambda x: x['total'], reverse=True)
    
    # Encontrar la posición del usuario actual
    user_position = next((i+1 for i, item in enumerate(ranking) if item['user'].id == request.user.id), '-')
    
    # Calcular días restantes en la quincena
    days_left = 15 - (today.day % 15)
    if days_left == 15:
        days_left = 0
    
    # Obtener puntos del usuario actual
    current_user_points = user_points.get(request.user.id, {
        'total': 0, 
        'activities_count': 0,
        'by_type': {}
    })
    
    # Obtener puntos por tipo para el usuario actual
    commit_points = current_user_points['by_type'].get('commit', 0)
    sprint_points = current_user_points['by_type'].get('sprint', 0)
    early_points = current_user_points['by_type'].get('early', 0)
    system_points = current_user_points['by_type'].get('system', 0)
    
    context = {
        'period': period,
        'total_points': sum(item['total'] for item in user_points.values()),
        'user_position': user_position,
        'days_left': days_left,
        'ranking': ranking,
        'user_points': {
            'total': current_user_points['total'],
            'commit': commit_points,
            'sprint': sprint_points,
            'early': early_points,
            'system': system_points
        },
    }
    
    return render(request, 'dashboard/dashboard.html', context)