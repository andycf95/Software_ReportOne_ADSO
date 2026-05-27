from django.db import models

# Create your models here.
class Activo(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    modelo = models.CharField(max_length=100, blank=True)
    marca = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    fecha_adquisicion = models.DateField(null=True, blank=True)
    estado_operativo = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.marca} {self.nombre}" if self.marca else self.nombre
    
    class Meta:
        verbose_name = "Activo"
        verbose_name_plural = "Activos"
    
class Sistema(models.Model):
    activo = models.ForeignKey(
        Activo, 
        on_delete=models.CASCADE, # Si se elimina el activo, se eliminan sus sistemas lógicos
        related_name="sistemas", 
        verbose_name="Activo Asociado"
    )
    nombre = models.CharField(max_length=100)
    tipo_sistema = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = "Sistema"
        verbose_name_plural = "Sistemas"

class SubSistema(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    sistema = models.ForeignKey(Sistema, on_delete=models.CASCADE, related_name='subsistemas')

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = "Subsistema"
        verbose_name_plural = "Subsistemas"