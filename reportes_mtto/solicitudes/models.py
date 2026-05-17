from django.db import models

# Create your models here.


class Solicitud(models.Model):

    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En proceso'),
        ('CERRADA', 'Cerrada'),
    ]

    CRITICIDAD = [
            (1, '1 - Baja'),
            (2, '2 - Media'),
            (3, '3 - Alta'),
            (4, '4 - Crítica'),
            (5, '5 - Emergencia'),
            
    ]

    usuario = models.CharField(
        max_length=100
    )

    activo = models.CharField(
        max_length=100
    )

    sistemaActivo = models.CharField(
        max_length=100
    )

    subsistemaActivo = models.CharField(
        max_length=100
    )

    titulo = models.CharField(
        max_length=100
    )

    descripcion = models.TextField()
    
    repuestosNecesarios = models.TextField()

    criticidad = models.IntegerField(
        max_length=10,
        choices=CRITICIDAD
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='PENDIENTE'
    )

    fechaCreacion = models.DateTimeField(
        auto_now_add=True
    )

    fechaActualizacion = models.DateTimeField(
        auto_now=True
    )

    fechaCierre = models.DateTimeField(
        null=True,
        blank=True
    )

    trabajoRealizado = models.TextField(
        null=True,
        blank=True
    )

    observacionesCierre = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.titulo