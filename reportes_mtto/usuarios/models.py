from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        SUPERVISOR = 'SUPERVISOR', 'Supervisor'
        TECNICO = 'TECNICO', 'Técnico'
        
    rol = models.CharField( max_length=20, choices=Rol.choices, default=Rol.TECNICO)
    correo = models.CharField(max_length=20, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    numero_identificacion = models.CharField( max_length=20, unique=True, verbose_name='Número de identificación')


    def __str__(self):
        return self.username