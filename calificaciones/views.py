from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
#from .models import Curso
#from .utils import calcular_promedio

# Create your views here.

# calificaciones/views.py
@login_required
def dashboard(request):
    context = {}
    if hasattr(request.user, 'es_estudiante') and request.user.es_estudiante:
        context['promedio'] = calcular_promedio(request.user)
    elif hasattr(request.user, 'es_profesor') and request.user.es_profesor:
        context['cursos_count'] = Curso.objects.filter(profesor=request.user).count()
    return render(request, 'dashboard.html', context)

def perfil_view(request):
    context = {
        'usuario': request.user
    }
    return render(request, 'perfil.html', context)

class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'