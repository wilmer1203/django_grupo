# Register your models here.

from django.contrib import admin
from .models import Estudiante, Curso, Calificacion

admin.site.register(Estudiante)
admin.site.register(Curso)
admin.site.register(Calificacion)