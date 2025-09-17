from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Activity, ActivityType
from users.models import User

@login_required
def add_activity(request):
    if not request.user.is_admin:
        messages.error(request, 'No tienes permisos para realizar esta acción')
        return redirect('dashboard:dashboard')
    
    activity_types = ActivityType.objects.all()
    users = User.objects.filter(rol=User.USER)
    
    if request.method == 'POST':
        activity_type_id = request.POST.get('activity_type')
        user_id = request.POST.get('user')
        date = request.POST.get('date')
        time = request.POST.get('time')
        evidence = request.POST.get('evidence')
        notes = request.POST.get('notes')
        
        try:
            activity_type = ActivityType.objects.get(id=activity_type_id)
            user = User.objects.get(id=user_id)
            
            # Combinar fecha y hora
            datetime_str = f"{date} {time}"
            
            activity = Activity(
                activity_type=activity_type,
                user=user,
                date=date,
                evidence=evidence,
                note=notes
            )
            activity.save()
            
            messages.success(request, 'Actividad registrada correctamente')
            return redirect('activities:add_activity')
            
        except Exception as e:
            messages.error(request, f'Error al registrar la actividad: {str(e)}')
    
    context = {
        'activity_types': activity_types,
        'users': users,
    }
    return render(request, 'activities/add_activity.html', context)

@login_required
def activity_list(request):
    activities = Activity.objects.all().order_by('-date', '-created_at')
    context = {
        'activities': activities
    }
    return render(request, 'activities/activity_list.html', context)