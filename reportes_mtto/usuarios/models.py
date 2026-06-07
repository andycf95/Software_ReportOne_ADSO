from django.contrib.auth.models import AbstractUser
from django.db import models

# Modelo de usuario personalizado que extiende AbstractUser para agregar campos adicionales como rol, correo, teléfono y número de identificación
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
    #Asignacion de activo a un tecnico 
    activo_asignado = models.OneToOneField(
        'activos.Activo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tecnico_asignado',
        verbose_name='Activo asignado'
    )

    def save(self, *args, **kwargs):
    # Si el usuario está inactivo no puede tener activo asignado
        if not self.is_active and self.activo_asignado:
            self.activo_asignado = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username