from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

#Se crea modelo para solicitud de mantenimiento, con campos para título, descripción, estado, criticidad, activo, sistema activo y subsistema activo
class Solicitud(models.Model):

    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En proceso'),
        ('CERRADA', 'Cerrada'),
    ]

    CRITICIDAD = [
            (1, 'Baja'),
            (2, 'Media'),
            (3, 'Alta'),
            (4, 'Crítica'),
            (5, 'Emergencia'),
            
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='solicitudes_creadas',
        null=True,
        blank=True
    )

    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True)
    activo = models.CharField(max_length=100)
    sistema_activo = models.CharField(max_length=100)
    subsistema_activo = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    repuestos_necesarios = models.TextField()
    criticidad = models.IntegerField( choices=CRITICIDAD, default=1)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    trabajo_realizado = models.TextField(null=True, blank=True)
    observaciones_cierre = models.TextField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        creando = self.pk is None

        super().save(*args, **kwargs)

        if creando and not self.codigo:
            self.codigo = f"RQ-{self.id:03d}"
            super().save(update_fields=['codigo'])
            
    def iniciar_proceso(self):
        if self.estado != 'PENDIENTE':
            raise ValueError('Solo una solicitud pendiente puede iniciar proceso.')
        self.estado = 'EN_PROCESO'
        self.save()
        
    def cerrar(self, trabajo_realizado, observaciones_cierre=""):
        if self.estado != 'EN_PROCESO':
            raise ValueError('Solo una solicitud en proceso puede cerrarse.')

        self.trabajo_realizado = trabajo_realizado
        self.observaciones_cierre = observaciones_cierre
        self.fecha_cierre = timezone.now()
        self.estado = 'CERRADA'
        self.save()
        
    def delete(self, *args, **kwargs):
        if self.estado != 'PENDIENTE':
            raise ValueError('Solo se pueden eliminar solicitudes pendientes.')
        super().delete(*args, **kwargs)    
        
    def __str__(self):
        return f"{self.codigo} - {self.titulo}"
    
# Agregar clase para seguimiento de solicitudes, con relación a la clase Solicitud y campos para comentario y fecha de seguimiento
class Seguimiento(models.Model):
    solicitud = models.ForeignKey(
            Solicitud,
            on_delete=models.CASCADE,
            related_name='seguimientos'
        )
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Seguimiento de {self.solicitud.titulo}"