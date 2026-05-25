from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = (
        'username',
        'numero_identificacion',
        'first_name',
        'last_name',
        'email',
        'rol',
        'telefono',
        'is_active',
        'is_staff',
    )

    list_filter = (
        'rol',
        'is_active',
        'is_staff',
        'is_superuser',
    )

    search_fields = (
        'username',
        'numero_identificacion',
        'first_name',
        'last_name',
        'email',
        'telefono',
    )

    ordering = (
        'username',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': (
                'numero_identificacion',
                'telefono',
                'rol',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {
            'fields': (
                'numero_identificacion',
                'email',
                'first_name',
                'last_name',
                'telefono',
                'rol',
            )
        }),
    )