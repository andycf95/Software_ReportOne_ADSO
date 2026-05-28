from django.db import models
import time

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
    codigo = models.CharField(max_length=20, unique=True, blank=True)
    tipo_sistema = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    
    
    def save(self, *args, **kwargs):
        creando = self.pk is None

        # Evitamos choques de campos vacíos con el unique=True en cargas masivas
        if creando and not self.codigo:
            self.codigo = f"TEMP-SIS-{int(time.time() * 1000)}"

        # Guarda para generar el ID real en la base de datos
        super().save(*args, **kwargs)

        # Si tenía el código temporal, lo reemplazamos con su ID definitivo
        if creando and self.codigo.startswith("TEMP-SIS-"):
            self.codigo = f"SIS-{self.id:03d}"
            super().save(update_fields=['codigo'])

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = "Sistema"
        verbose_name_plural = "Sistemas"
        
        

class Componente(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    sistema = models.ForeignKey(Sistema, on_delete=models.CASCADE, related_name='componentes')
    modelo = models.CharField(max_length=100, blank=True)
    marca = models.CharField(max_length=100, blank=True)
    
    def save(self, *args, **kwargs):
        creando = self.pk is None

        if creando and not self.codigo:
            self.codigo = f"TEMP-COM-{int(time.time() * 1000)}"

        # Guarda para generar el ID real
        super().save(*args, **kwargs)

        # Reemplaza el temporal por el código definitivo secuencial
        if creando and self.codigo.startswith("TEMP-COM-"):
            self.codigo = f"COM-{self.id:03d}"
            super().save(update_fields=['codigo', 'marca', 'modelo'])

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = "Componente"
        verbose_name_plural = "Componentes"