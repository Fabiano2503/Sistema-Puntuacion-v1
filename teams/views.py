from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Team
from users.models import User

@login_required
def team_management(request):
    if not request.user.is_admin:
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('dashboard:dashboard')
    
    teams = Team.objects.annotate(
        calculated_points=Sum('user__activity__activity_type__points')
    )
    
    context = {
        'teams': teams
    }
    return render(request, 'teams/team_management.html', context)

@login_required
def add_team(request):
    if not request.user.is_admin:
        messages.error(request, 'No tienes permisos para realizar esta acción')
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if Team.objects.filter(name=name).exists():
            messages.error(request, 'Ya existe un equipo con ese nombre')
        else:
            team = Team(name=name, description=description)
            team.save()
            messages.success(request, 'Equipo creado correctamente')
        
        return redirect('teams:team_management')
    
    return render(request, 'teams/add_team.html')

@login_required
def edit_team(request, team_id):
    if not request.user.is_admin:
        messages.error(request, 'No tienes permisos para realizar esta acción')
        return redirect('dashboard:dashboard')
    
    team = get_object_or_404(Team, id=team_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        # Verificar si el nombre ya existe (excluyendo el equipo actual)
        if Team.objects.filter(name=name).exclude(id=team_id).exists():
            messages.error(request, 'Ya existe un equipo con ese nombre')
        else:
            team.name = name
            team.description = description
            team.save()
            messages.success(request, 'Equipo actualizado correctamente')
        
        return redirect('teams:team_management')
    
    context = {
        'team': team
    }
    return render(request, 'teams/edit_team.html', context)

@login_required
def delete_team(request, team_id):
    if not request.user.is_admin:
        messages.error(request, 'No tienes permisos para realizar esta acción')
        return redirect('dashboard:dashboard')
    
    team = get_object_or_404(Team, id=team_id)
    
    # Verificar si hay usuarios en este equipo
    users_in_team = User.objects.filter(team=team)
    if users_in_team.exists():
        messages.error(request, 'No se puede eliminar el equipo porque tiene usuarios asignados')
    else:
        team.delete()
        messages.success(request, 'Equipo eliminado correctamente')
    
    return redirect('teams:team_management')