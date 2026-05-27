# cargar_datos.py

import os
import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reportes_mtto.settings")
django.setup()

from activos.models import Activo, Sistema, SubSistema

# Limpiar datos existentes (opcional)
SubSistema.objects.all().delete()
Sistema.objects.all().delete()
Activo.objects.all().delete()

activos_data = [
    {
        "codigo": "ACT-0001",
        "nombre": "Remolcador Atlas",
        "marca": "Caterpillar",
        "modelo": "RT-500",
        "sistemas": [
            {
                "nombre": "Sistema de Propulsión",
                "subsistemas": [
                    "Motor Principal",
                    "Caja Reductora",
                    "Eje de Transmisión",
                    "Hélice"
                ]
            },
            {
                "nombre": "Sistema Eléctrico",
                "subsistemas": [
                    "Generador Principal",
                    "Banco de Baterías",
                    "Tablero General",
                    "Sistema de Iluminación"
                ]
            },
            {
                "nombre": "Sistema Hidráulico",
                "subsistemas": [
                    "Bomba Hidráulica",
                    "Válvulas de Control",
                    "Mangueras",
                    "Tanque Hidráulico"
                ]
            },
            {
                "nombre": "Sistema de Combustible",
                "subsistemas": [
                    "Tanque de Combustible",
                    "Bomba de Transferencia",
                    "Filtros",
                    "Inyectores"
                ]
            }
        ]
    },
    {
        "codigo": "ACT-0002",
        "nombre": "Barcaza Delta",
        "marca": "Volvo Penta",
        "modelo": "BD-300",
        "sistemas": [
            {
                "nombre": "Sistema de Propulsión",
                "subsistemas": [
                    "Motor Auxiliar",
                    "Caja de Engranajes",
                    "Eje Principal",
                    "Hélice Auxiliar"
                ]
            },
            {
                "nombre": "Sistema Eléctrico",
                "subsistemas": [
                    "Generador Auxiliar",
                    "UPS",
                    "Tablero Secundario",
                    "Luces de Navegación"
                ]
            },
            {
                "nombre": "Sistema Contra Incendios",
                "subsistemas": [
                    "Bombas",
                    "Extintores",
                    "Sensores",
                    "Alarmas"
                ]
            },
            {
                "nombre": "Sistema de Agua",
                "subsistemas": [
                    "Tanque de Agua",
                    "Bomba de Agua",
                    "Filtros",
                    "Tuberías"
                ]
            }
        ]
    },
    {
        "codigo": "ACT-0003",
        "nombre": "Grúa Portuaria GX",
        "marca": "Liebherr",
        "modelo": "GX-900",
        "sistemas": [
            {
                "nombre": "Sistema de Izaje",
                "subsistemas": [
                    "Cable Principal",
                    "Gancho",
                    "Poleas",
                    "Tambor"
                ]
            },
            {
                "nombre": "Sistema Eléctrico",
                "subsistemas": [
                    "Motor Eléctrico",
                    "Transformador",
                    "Tablero de Control",
                    "Sensores"
                ]
            },
            {
                "nombre": "Sistema Hidráulico",
                "subsistemas": [
                    "Cilindros",
                    "Bombas",
                    "Válvulas",
                    "Depósito"
                ]
            },
            {
                "nombre": "Sistema de Seguridad",
                "subsistemas": [
                    "Cámaras",
                    "Alarmas",
                    "Limitadores",
                    "Botón de Emergencia"
                ]
            }
        ]
    }
]

for activo_data in activos_data:

    activo = Activo.objects.create(
        codigo=activo_data["codigo"],
        nombre=activo_data["nombre"],
        marca=activo_data["marca"],
        modelo=activo_data["modelo"],
        descripcion=f"Activo {activo_data['nombre']}"
    )

    print(f"Activo creado: {activo.nombre}")

    for sistema_data in activo_data["sistemas"]:

        sistema = Sistema.objects.create(
            activo=activo,
            nombre=sistema_data["nombre"],
            descripcion=f"Sistema {sistema_data['nombre']}"
        )

        print(f"  Sistema creado: {sistema.nombre}")

        for nombre_subsistema in sistema_data["subsistemas"]:

            SubSistema.objects.create(
                sistema=sistema,
                nombre=nombre_subsistema,
                descripcion=f"Subsistema {nombre_subsistema}"
            )

            print(f"    Subsistema creado: {nombre_subsistema}")

print("\nCarga de datos finalizada correctamente.")