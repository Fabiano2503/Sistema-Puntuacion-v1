from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import User
from teams.models import Team

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, 'Credenciales incorrectas')
    
    return render(request, 'users/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('users:login')

@login_required
def user_management(request):
    if not request.user.is_admin:
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('dashboard:dashboard')
    
    users = User.objects.all()
    teams = Team.objects.all()
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        team_id = request.POST.get('team')
        role = request.POST.get('role')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if user_id:  # Editar usuario existente
            user = get_object_or_404(User, id=user_id)
            user.name = name
            user.email = email
            user.team = Team.objects.get(id=team_id) if team_id else None
            user.rol = role
            user.save()
            messages.success(request, 'Usuario actualizado correctamente')
        else:  # Crear nuevo usuario
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Ya existe un usuario con este email')
            elif not password or not password_confirm:
                messages.error(request, 'Debes ingresar y confirmar la contraseña')
            elif password != password_confirm:
                messages.error(request, 'Las contraseñas no coinciden')
            else:
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    name=name,
                    team=Team.objects.get(id=team_id) if team_id else None,
                    rol=role
                )
                messages.success(request, 'Usuario creado correctamente')

        return redirect('users:user_management')

    context = {
        'users': users,
        'teams': teams,
    }
    return render(request, 'users/management.html', context)

@login_required
def edit_user(request, user_id):
    if not request.user.is_admin:
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('dashboard:dashboard')
    
    user = get_object_or_404(User, id=user_id)
    users = User.objects.all()
    teams = Team.objects.all()
    
    context = {
        'editing_user': user,
        'users': users,
        'teams': teams,
    }
    return render(request, 'users/management.html', context)

@login_required
def delete_user(request, user_id):
    if not request.user.is_admin:
        messages.error(request, 'No tienes permisos para realizar esta acción')
        return redirect('dashboard:dashboard')
    
    user = get_object_or_404(User, id=user_id)
    
    # No permitir eliminarse a sí mismo
    if user == request.user:
        messages.error(request, 'No puedes eliminarte a ti mismo')
    else:
        user.delete()
        messages.success(request, 'Usuario eliminado correctamente')
    
    return redirect('users:user_management')