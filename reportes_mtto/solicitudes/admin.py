from django.contrib import admin
from .models import Solicitud
from .models import Seguimiento

# Register your models here.


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('codigo','usuario' , 'titulo', 'estado', 'fecha_creacion')
    readonly_fields = ('estado', 'fecha_creacion', 'fecha_cierre')

    def has_delete_permission(self, request, obj=None):
        if obj and obj.estado != 'PENDIENTE':
            return False
        return super().has_delete_permission(request, obj)
    

@admin.register(Seguimiento)
class SeguimientoAdmin(admin.ModelAdmin):
    list_display = ('solicitud', 'fecha', 'comentario')
    readonly_fields = ('solicitud', 'comentario', 'fecha')

    def has_delete_permission(self, request, obj=None):
        return False