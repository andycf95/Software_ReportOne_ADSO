from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Activo, Sistema, SubSistema

@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'modelo')

@admin.register(Sistema)
class SistemaAdmin(admin.ModelAdmin):
    list_display = ('activo', 'nombre', 'tipo_sistema')

@admin.register(SubSistema)
class SubSistemaAdmin(admin.ModelAdmin):
    list_display = ('sistema', 'nombre')