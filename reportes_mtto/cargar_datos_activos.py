# cargar_datos.py

import os
import django
import time
from django.db import connection
# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reportes_mtto.settings")
django.setup()

from activos.models import Activo, Sistema, Componente

# Limpiar datos existentes
print("Limpiando base de datos...")
Componente.objects.all().delete()
Sistema.objects.all().delete()
Activo.objects.all().delete()

with connection.cursor() as cursor:
    cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name IN ('activos_activo', 'activos_sistema', 'activos_componente');")
print("Contadores de ID reseteados a cero.")

# Estructura con 4 activos reales y sus fichas técnicas completas
activos_data = [
    {
        "codigo": "ACT-0001",
        "nombre": "Remolcador Atlas",
        "marca": "Caterpillar",
        "modelo": "RT-500",
        "sistemas": [
            {
                "nombre": "Sistema de Propulsión",
                "tipo_sistema": "Mecánico/Principal",
                "componentes": [
                    {"nombre": "Motor Principal", "marca": "Caterpillar", "modelo": "3516C"},
                    {"nombre": "Caja Reductora", "marca": "Reintjes", "modelo": "WAF 863"},
                    {"nombre": "Eje de Transmisión", "marca": "Custom Steel", "modelo": "Shaft-V1"},
                    {"nombre": "Hélice Azimutal", "marca": "Schottel", "modelo": "SRP 1212"}
                ]
            },
            {
                "nombre": "Sistema Eléctrico",
                "tipo_sistema": "Eléctrico",
                "componentes": [
                    {"nombre": "Generador Principal", "marca": "John Deere", "modelo": "4045AFM85"},
                    {"nombre": "Banco de Baterías", "marca": "Bosch", "modelo": "S5 12V"},
                    {"nombre": "Tablero General", "marca": "Schneider", "modelo": "Prisma P"},
                    {"nombre": "Sistema de Iluminación", "marca": "Philips", "modelo": "LED Marine"}
                ]
            },
            {
                "nombre": "Sistema Hidráulico",
                "tipo_sistema": "Hidráulico",
                "componentes": [
                    {"nombre": "Bomba Hidráulica", "marca": "Rexroth", "modelo": "A10VSO"},
                    {"nombre": "Válvulas de Control", "marca": "Vickers", "modelo": "DG4V"},
                    {"nombre": "Mangueras de Alta Presión", "marca": "Parker", "modelo": "No-Skive"},
                    {"nombre": "Tanque Hidráulico", "marca": "Custom", "modelo": "T-200L"}
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
                "nombre": "Sistema de Propulsión Auxiliar",
                "tipo_sistema": "Mecánico/Auxiliar",
                "componentes": [
                    {"nombre": "Motor Auxiliar", "marca": "Volvo Penta", "modelo": "D13"},
                    {"nombre": "Caja de Engranajes", "marca": "ZF", "modelo": "ZF 325"},
                    {"nombre": "Eje Principal", "marca": "Marine Steel", "modelo": "MS-200"},
                    {"nombre": "Hélice de Maniobra", "marca": "Michigan Wheel", "modelo": "MP-3"}
                ]
            },
            {
                "nombre": "Sistema Contra Incendios",
                "tipo_sistema": "Seguridad/Fluidos",
                "componentes": [
                    {"nombre": "Bomba Contra Incendios", "marca": "Aurora", "modelo": "411-Series"},
                    {"nombre": "Estación de Extintores CO2", "marca": "Badger", "modelo": "CO2-10"},
                    {"nombre": "Sensores de Humo", "marca": "Honeywell", "modelo": "FSP-851"},
                    {"nombre": "Alarma Sonora", "marca": "System Sensor", "modelo": "SS-24v"}
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
                "tipo_sistema": "Mecánico/Estructura",
                "componentes": [
                    {"nombre": "Cable Principal de Acero", "marca": "Liebherr", "modelo": "C-25MM"},
                    {"nombre": "Gancho de Carga", "marca": "RopeBlock", "modelo": "RB-150T"},
                    {"nombre": "Poleas de Reenvío", "marca": "Liebherr", "modelo": "P-450"},
                    {"nombre": "Tambor de Enrollado", "marca": "Custom Heavy", "modelo": "T-900"}
                ]
            },
            {
                "nombre": "Sistema de Control Eléctrico",
                "tipo_sistema": "Electrónico",
                "componentes": [
                    {"nombre": "Variador de Frecuencia", "marca": "Siemens", "modelo": "Sinamics G120"},
                    {"nombre": "PLC de Control", "marca": "Siemens", "modelo": "S7-1500"},
                    {"nombre": "Joystick de Cabina", "marca": "Gessmann", "modelo": "V6/VV6"},
                    {"nombre": "Anemómetro Digital", "marca": "Davis Instruments", "modelo": "Vantage Pro"}
                ]
            }
        ]
    },
    {
        "codigo": "ACT-0004",
        "nombre": "Remolcador Tritón",
        "marca": "Wärtsilä",
        "modelo": "WT-800",
        "sistemas": [
            {
                "nombre": "Sistema de Generación de Potencia",
                "tipo_sistema": "Térmico/Eléctrico",
                "componentes": [
                    {"nombre": "Motor Generador Diésel", "marca": "Wärtsilä", "modelo": "6L20"},
                    {"nombre": "Alternador Principal", "marca": "Leroy Somer", "modelo": "LSA 52.3"},
                    {"nombre": "Regulador de Voltaje (AVR)", "marca": "Basler", "modelo": "DECS-150"},
                    {"nombre": "Radiador de Enfriamiento", "marca": "Kranji", "modelo": "RAD-WT800"}
                ]
            },
            {
                "nombre": "Sistema de Gobierno (Timón)",
                "tipo_sistema": "Mecánico/Hidráulico",
                "componentes": [
                    {"nombre": "Servo Timón Hidráulico", "marca": "Rolls-Royce", "modelo": "SR622"},
                    {"nombre": "Pala de Timón", "marca": "Astillero Central", "modelo": "P-WT8"},
                    {"nombre": "Bomba de Timón", "marca": "Eaton", "modelo": "PVH98"},
                    {"nombre": "Transmisor de Ángulo", "marca": "Kongsberg", "modelo": "RA-45"}
                ]
            }
        ]
    }
]

print("\nIniciando carga masiva de 4 activos...")

for activo_data in activos_data:
    # Creamos el Activo
    activo = Activo.objects.create(
        codigo=activo_data["codigo"],
        nombre=activo_data["nombre"],
        marca=activo_data["marca"],
        modelo=activo_data["modelo"],
        descripcion=f"Activo {activo_data['nombre']} de alto rendimiento operacional."
    )
    print(f"✅ Activo creado: {activo.nombre} [{activo.codigo}]")

    for sistema_data in activo_data["sistemas"]:
        # Creamos el Sistema asociado
        sistema = Sistema.objects.create(
            activo=activo,
            nombre=sistema_data["nombre"],
            tipo_sistema=sistema_data["tipo_sistema"],
            descripcion=f"Sistema de categoría {sistema_data['tipo_sistema']}"
        )
        
        time.sleep(0.001) # Pausa de seguridad para evitar colisiones en milisegundos
        print(f"  ⚙️ Sistema creado: {sistema.nombre} [{sistema.codigo}]")

        for comp_data in sistema_data["componentes"]:
            # Creamos el Componente asociado
            componente = Componente.objects.create(
                sistema=sistema,
                nombre=comp_data["nombre"],
                marca=comp_data["marca"],
                modelo=comp_data["modelo"],
                descripcion=f"Componente industrial modelo {comp_data['modelo']}"
            )
            
            time.sleep(0.001) # Pausa de seguridad
            print(f"    🔧 Componente creado: {componente.nombre} -> {componente.marca} {componente.modelo} [{componente.codigo}]")

print("\n🚀 ¡Carga masiva finalizada con éxito! Los 4 activos están listos en la base de datos.")