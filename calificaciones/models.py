from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

class UsuarioPersonalizado(AbstractUser):
    ROLES = (
        ('E', 'Estudiante'),
        ('P', 'Profesor'),
        ('A', 'Administrador'),
    )
    rol = models.CharField(max_length=1, choices=ROLES, default='E')
    
class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    profesor = models.ForeignKey(UsuarioPersonalizado, on_delete=models.SET_NULL, null=True)

class Calificacion(models.Model):
    estudiante = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=5, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)