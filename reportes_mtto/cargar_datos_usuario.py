# crear_usuarios.py

import os
import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reportes_mtto.settings")
django.setup()

from django.contrib.auth import get_user_model
Usuario = get_user_model()

print("Iniciando creación de usuarios personalizados...")

# Datos estructurados con los campos exactos de tu modelo
usuarios_data = [
    {
        "username": "tecnico_prueba",
        "email": "tecnico@fixly.com",
        "rol": Usuario.Rol.TECNICO,                  # 💡 Usa tu TextChoices
        "numero_identificacion": "1000000001",       # 💡 Campo obligatorio único
        "telefono": "3001112222",
        "es_admin": False
    },
    {
        "username": "supervisor_prueba",
        "email": "supervisor@fixly.com",
        "rol": Usuario.Rol.SUPERVISOR,
        "numero_identificacion": "1000000002",
        "telefono": "3003334444",
        "es_admin": False
    },
    {
        "username": "administrador_prueba",
        "email": "admin@fixly.com",
        "rol": Usuario.Rol.ADMIN,
        "numero_identificacion": "1000000003",
        "telefono": "3005556666",
        "es_admin": True
    }
]

clave_comun = "Prueba1234"

for u_data in usuarios_data:
    # Evitar errores por duplicados si el script se corre dos veces
    if Usuario.objects.filter(username=u_data["username"]).exists():
        print(f"⚠️ El usuario '{u_data['username']}' ya existe. Saltando...")
        continue

    if u_data["es_admin"]:
        # Creamos el Administrador como Superusuario de Django
        usuario = Usuario.objects.create_superuser(
            username=u_data["username"],
            email=u_data["email"],
            password=clave_comun,
            rol=u_data["rol"],
            numero_identificacion=u_data["numero_identificacion"],
            telefono=u_data["telefono"]
        )
    else:
        # Creamos los usuarios estándar (Técnico y Supervisor)
        usuario = Usuario.objects.create_user(
            username=u_data["username"],
            email=u_data["email"],
            password=clave_comun,
            rol=u_data["rol"],
            numero_identificacion=u_data["numero_identificacion"],
            telefono=u_data["telefono"]
        )

    print(f"✅ Usuario creado: {usuario.username} | Rol: {usuario.rol} | ID: {usuario.numero_identificacion}")

print("\n🚀 ¡Todos los usuarios listos con sus respectivos roles y la contraseña 'Prueba1234'!")