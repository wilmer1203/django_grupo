from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.db.models import Avg
from .models import UsuarioPersonalizado, Calificacion, Curso

def redireccion_rol(request):
    if request.user.rol == 'E':
        return redirect('perfil_estudiante')
    elif request.user.rol in ['P']:
        return redirect('gestion_calificaciones')
    elif request.user.rol in ['A']:
        return redirect('/admin')
    return redirect('dashboard')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def perfil_estudiante(request):
    if request.user.rol != 'E':
        messages.error(request, 'Acceso restringido a estudiantes')
        return redirect('dashboard')
    
    calificaciones = Calificacion.objects.filter(estudiante=request.user).select_related('curso')
    promedio = calificaciones.aggregate(
    promedio=Avg('nota'))['promedio'] or 0  # Valor por defecto si no hay calificaciones
    
    return render(request, 'perfil_estudiante.html', {
        'calificaciones': calificaciones,
        'promedio': calificaciones.aggregate(Avg('nota'))['nota__avg']
    })

@login_required
def gestion_calificaciones(request, calificacion_id=None):
    # Verificación de roles
    if request.user.rol not in ['P']:
        messages.error(request, 'Acceso restringido a profesores')
        return redirect('dashboard')
    
    # Configuración inicial
    editar = False
    instance = None
    cursos = Curso.objects.all()
    
    # Filtros por rol
    if request.user.rol == 'P':
        cursos = cursos.filter(profesor=request.user)
    
    estudiantes = UsuarioPersonalizado.objects.filter(rol='E') if request.user.rol == 'P' else None
    calificaciones = Calificacion.objects.filter(curso__profesor=request.user) if request.user.rol == 'P' else Calificacion.objects.all()
    calificaciones = calificaciones.select_related('curso', 'estudiante')
    
    # Manejo de edición
    if calificacion_id:
        instance = get_object_or_404(Calificacion, id=calificacion_id)
        editar = True
        
        # Verificar permisos para edición
        if request.user.rol == 'P' and instance.curso.profesor != request.user:
            messages.error(request, 'No tienes permiso para editar esta calificación')
            return redirect('gestion_calificaciones')

    # Procesamiento de formulario
    if request.method == 'POST':
        # Manejar eliminación
        if 'eliminar' in request.POST:
            return eliminar_calificacion(request, request.POST.get('calificacion_id'))
            
        # Validar y procesar datos
        try:
            data = {
                'estudiante_id': request.POST.get('estudiante') or request.user.id,
                'curso_id': request.POST.get('curso'),
                'nota': request.POST.get('nota')
            }
            
            if not all(data.values()):
                raise ValueError("Todos los campos son requeridos")
                
            if instance:
                # Actualización
                Calificacion.objects.filter(id=calificacion_id).update(**data)
                messages.success(request, 'Calificación actualizada correctamente')
            else:
                # Creación
                Calificacion.objects.create(**data)
                messages.success(request, 'Calificación creada correctamente')
                
            return redirect('gestion_calificaciones')
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    context = {
        'editar': editar,
        'cursos': cursos,
        'estudiantes': estudiantes,
        'calificaciones': calificaciones,
        'form': instance
    }
    return render(request, 'gestion_calificaciones.html', context)

@login_required
def eliminar_calificacion(request, calificacion_id):
    if request.method == 'POST':
        calificacion = get_object_or_404(Calificacion, id=calificacion_id)
        
        # Verificar permisos para eliminación
        if request.user.rol == 'P' and calificacion.curso.profesor != request.user:
            messages.error(request, 'No tienes permiso para eliminar esta calificación')
            return redirect('gestion_calificaciones')
            
        calificacion.delete()
        messages.success(request, 'Calificación eliminada correctamente')
    return redirect('gestion_calificaciones')

class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'