from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UsuarioPersonalizado(AbstractUser):
    es_estudiante = models.BooleanField(default=False)
    es_profesor = models.BooleanField(default=False)
    es_administrador = models.BooleanField(default=False)
    