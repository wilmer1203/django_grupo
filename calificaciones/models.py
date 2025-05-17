from django.db import models
from django.contrib.auth.models import AbstractUser, User


# Create your models here.
class UsuarioPersonalizado(AbstractUser):
    es_estudiante = models.BooleanField(default=False)
    es_profesor = models.BooleanField(default=False)
    es_administrador = models.BooleanField(default=False)
    
class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación con usuario
    numero_identificacion = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    profesor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre

class Calificacion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=5, decimal_places=2)  # Ej: 9.50
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante} - {self.curso}: {self.nota}"
