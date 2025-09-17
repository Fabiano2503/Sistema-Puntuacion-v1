from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import io
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
    
    def normalize_type_key(raw_name: str) -> str:
        n = (raw_name or '').strip().lower()
        # Spanish-friendly normalization
        if 'commit' in n:
            return 'commit'
        if 'sprint' in n or 'review' in n:
            return 'sprint'
        if 'tempran' in n or 'puntual' in n or 'puntualidad' in n or 'temprano' in n:
            return 'early'
        if 'completar' in n or 'sistema' in n:
            return 'system'
        return n or 'otros'

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
    
        # Contar por tipo de actividad (normalizado)
        type_key = normalize_type_key(activity.activity_type.name)
        if type_key not in user_points[user_id]['by_type']:
            user_points[user_id]['by_type'][type_key] = 0
        user_points[user_id]['by_type'][type_key] += activity.activity_type.points
    
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


@login_required
def export_ranking_excel(request):
    period = request.GET.get('period', 'diario')

    today = timezone.now().date()
    if period == 'diario':
        start_date = today
    elif period == 'semanal':
        start_date = today - timedelta(days=today.weekday())
    else:
        start_date = today - timedelta(days=14)

    activities = Activity.objects.filter(date__gte=start_date)

    # Build ranking same as dashboard
    user_data = {}
    for a in activities:
        uid = a.user.id
        if uid not in user_data:
            user_data[uid] = {
                'name': a.user.name,
                'team': a.user.team.name if getattr(a.user, 'team', None) else 'Sin equipo',
                'points': 0,
                'activities': 0,
            }
        user_data[uid]['points'] += a.activity_type.points
        user_data[uid]['activities'] += 1

    ranking = sorted(user_data.values(), key=lambda x: x['points'], reverse=True)

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="ranking.csv"'
    response.write('Posición,Nombre,Equipo,Puntos,Actividades\n')
    for idx, row in enumerate(ranking, start=1):
        response.write(f"{idx},{row['name']},{row['team']},{row['points']},{row['activities']}\n")
    return response


@login_required
def export_ranking_pdf(request):
    period = request.GET.get('period', 'diario')

    today = timezone.now().date()
    if period == 'diario':
        start_date = today
    elif period == 'semanal':
        start_date = today - timedelta(days=today.weekday())
    else:
        start_date = today - timedelta(days=14)

    activities = Activity.objects.filter(date__gte=start_date)

    user_data = {}
    for a in activities:
        uid = a.user.id
        if uid not in user_data:
            user_data[uid] = {
                'name': a.user.name,
                'team': a.user.team.name if getattr(a.user, 'team', None) else 'Sin equipo',
                'points': 0,
                'activities': 0,
            }
        user_data[uid]['points'] += a.activity_type.points
        user_data[uid]['activities'] += 1

    ranking = sorted(user_data.values(), key=lambda x: x['points'], reverse=True)

    # Generate PDF using fpdf2 (pure Python, no build tools)
    from fpdf import FPDF

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'Ranking', ln=1)

    # Header
    pdf.set_font('Helvetica', 'B', 10)
    headers = ['#', 'Nombre', 'Equipo', 'Puntos', 'Actividades']
    widths = [10, 60, 60, 25, 25]
    for h, w in zip(headers, widths):
        pdf.cell(w, 8, h, border=1, align='C')
    pdf.ln(8)

    # Rows
    pdf.set_font('Helvetica', '', 10)
    for idx, row in enumerate(ranking, start=1):
        cells = [str(idx), row['name'], row['team'], str(row['points']), str(row['activities'])]
        for c, w in zip(cells, widths):
            pdf.cell(w, 8, c, border=1, align='C')
        pdf.ln(8)

    output = bytes(pdf.output(dest='S'))
    buffer = io.BytesIO(output)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='ranking.pdf', content_type='application/pdf')