from django.db import models

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

    usuario = models.CharField(max_length=100)
    activo = models.CharField(max_length=100)
    sistema_activo = models.CharField(max_length=100)
    subsistema_activo = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    repuestos_necesarios = models.TextField()
    criticidad = models.IntegerField(max_length=10, choices=CRITICIDAD, default=1)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    trabajo_realizado = models.TextField(null=True, blank=True)
    observaciones_cierre = models.TextField(null=True, blank=True) 

    def __str__(self):
        return self.titulo
    
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