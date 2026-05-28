from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Activo, Sistema, Componente

@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'modelo')

@admin.register(Sistema)
class SistemaAdmin(admin.ModelAdmin):
    list_display = ('activo', 'nombre', 'tipo_sistema')

@admin.register(Componente)
class ComponenteAdmin(admin.ModelAdmin):
    list_display = ('sistema', 'nombre')