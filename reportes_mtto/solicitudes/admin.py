from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Solicitud, Seguimiento


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'usuario', 'activo', 'titulo', 'estado', 'criticidad', 'fecha_creacion', 'eliminado')
    readonly_fields = ('estado', 'fecha_creacion', 'fecha_cierre', 'eliminado')
    list_filter = ('estado', 'criticidad', 'eliminado')

    def get_queryset(self, request):
        return Solicitud.todos.all()

    def has_delete_permission(self, request, obj=None):
        if obj and obj.estado != 'PENDIENTE':
            return False
        return super().has_delete_permission(request, obj)

    def delete_model(self, request, obj):
        try:
            obj.delete()  
        except ValidationError as e:
            self.message_user(request, str(e), level=messages.ERROR)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            try:
                obj.delete()
            except ValidationError as e:
                self.message_user(request, f"{obj.codigo}: {e}", level=messages.ERROR)


@admin.register(Seguimiento)
class SeguimientoAdmin(admin.ModelAdmin):
    list_display = ('solicitud', 'fecha', 'comentario')
    readonly_fields = ('solicitud', 'comentario', 'fecha')

    def has_delete_permission(self, request, obj=None):
        return False 

    def has_add_permission(self, request):
        return False   