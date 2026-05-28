# cargar_solicitudes.py

import os
import django
import random
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reportes_mtto.settings")
django.setup()

# Importamos los modelos de las solicitudes y los activos
from solicitudes.models import Solicitud
from activos.models import Componente, Activo, Sistema

# 💡 SOLUCIÓN AL ERROR: Importamos el cargador dinámico del modelo de usuarios personalizado
from django.contrib.auth import get_user_model
User = get_user_model() 

# Limpiar solicitudes existentes para realizar una carga limpia de pruebas
print("Limpiando solicitudes anteriores de la base de datos...")
Solicitud.objects.all().delete()

# Banco de fallas típicas industriales para alimentar las 20 solicitudes de manera realista
fallas_banco = [
    {
        "buscar_comp": "Motor",
        "titulo": "Alta temperatura en block de cilindros",
        "descripcion": "Se detecta incremento anómalo de temperatura (95°C) en el sistema de camisas durante la operación. Se sospecha de obstrucción en línea de refrigeración o falla en termostato.",
        "criticidad": "1"
    },
    {
        "buscar_comp": "Caja",
        "titulo": "Vibración excesiva en caja reductora",
        "descripcion": "Operador reporta ruidos extraños y vibración fuera de los parámetros permisibles en la transmisión. Requiere análisis de alineación y revisión de piñones.",
        "criticidad": "5"
    },
    {
        "buscar_comp": "Bomba",
        "titulo": "Pérdida de presión en bomba hidráulica",
        "descripcion": "La presión del sistema cayó un 20% bajo carga nominal. Posible desgaste interno en los pistones de la bomba o cavitación por filtros sucios.",
        "criticidad": "4"
    },
    {
        "buscar_comp": "Generador",
        "titulo": "Fluctuación de voltaje en alternador",
        "descripcion": "El módulo de control registra caídas momentáneas de tensión. Es necesario revisar las escobillas, el regulador automático de voltaje (AVR) y conexiones.",
        "criticidad": "3"
    },
    {
        "buscar_comp": "Hélice",
        "titulo": "Inspección por posible daño en rampa de hélice",
        "descripcion": "Se solicita inspección subacuática o en seco debido a golpe reportado con objeto flotante. Se percibe leve pérdida de eficiencia en la navegación.",
        "criticidad": "5"
    },
    {
        "buscar_comp": "Válvulas",
        "titulo": "Fuga de fluido en válvula de control",
        "descripcion": "Goteo constante de aceite hidráulico en el sello del vástago de la válvula selectora. Requiere cambio urgente de empaquetaduras (O-rings).",
        "criticidad": "2"
    },
    {
        "buscar_comp": "Filtros",
        "titulo": "Saturación prematura de filtros de combustible",
        "descripcion": "Alarma de alta presión diferencial activada en el módulo Racor. Se requiere cambio de elementos filtrantes y verificar pureza del diésel en tanque.",
        "criticidad": "3"
    },
    {
        "buscar_comp": "Tablero",
        "titulo": "Disparo térmico en breaker principal",
        "descripcion": "El interruptor principal del tablero se disparó por sobrecorriente. Es necesario realizar termografía y verificar aislamiento de líneas.",
        "criticidad": "4"
    },
    {
        "buscar_comp": "Cable",
        "titulo": "Desgaste de hilos en cable de izaje",
        "descripcion": "Durante la inspección visual diaria se detectaron 3 hilos rotos en el paso del cable de acero de la grúa. Se solicita reemplazo por seguridad.",
        "criticidad": "1"
    },
    {
        "buscar_comp": "Mangueras",
        "titulo": "Desgaste por fricción en manguera hidráulica",
        "descripcion": "Manguera de alta presión presenta desprendimiento de la capa de caucho externa por roce continuo contra la estructura. Riesgo de estallido.",
        "criticidad": "5"
    }
]

estados_banco = ["PENDIENTE", "EN_PROCESO", "CERRADA"]

# Intentamos obtener el primer usuario disponible (que ahora será de tu app 'usuarios')
usuario_encargado = User.objects.first()

# Si la base de datos de usuarios está vacía, creamos uno administrador de pruebas automático
if not usuario_encargado:
    print("⚠️ No se encontró ningún usuario en la BD. Creando un usuario administrador automático...")
    usuario_encargado = User.objects.create_superuser(
        username="admin_prueba", 
        email="admin@fixly.com", 
        password="adminpassword123"
        # NOTA: Si tu modelo personalizado 'Usuario' tiene campos obligatorios extras,
        # agrégalos aquí (ej: cedula="12345", telefono="3001234567")
    )

# Cargamos los componentes disponibles generados por el script anterior
componentes_disponibles = list(Componente.objects.all())

if not componentes_disponibles:
    print("❌ Error: No hay componentes en la base de datos. Ejecuta primero cargar_datos.py")
else:
    print("\nIniciando inyección de 20 solicitudes con trazabilidad completa...")
    solicitudes_creadas = 0
    
    for i in range(1, 21):
        # Seleccionamos una falla aleatoria del banco
        falla_base = random.choice(fallas_banco)
        
        # Filtramos componentes de la BD que tengan relación semántica con la falla
        componentes_filtrados = Componente.objects.filter(nombre__icontains=falla_base["buscar_comp"])
        
        if componentes_filtrados.exists():
            componente_asignado = random.choice(componentes_filtrados)
        else:
            componente_asignado = random.choice(componentes_disponibles)
            
        # 💡 TRAZABILIDAD: Obtenemos el sistema y el activo directamente escalando por las llaves foráneas
        sistema_asignado = componente_asignado.sistema
        activo_asignado = sistema_asignado.activo
        
        estado_asignado = random.choice(estados_banco)
        
        # Generamos una fecha aleatoria dentro de los últimos 30 días para poblar el historial
        dias_atras = random.randint(0, 30)
        fecha_creacion = datetime.now() - timedelta(days=dias_atras)

        # Creamos la solicitud mapeando absolutamente todos los campos requeridos
        solicitud = Solicitud.objects.create(
            titulo=f"{falla_base['titulo']} #{i}",
            descripcion=falla_base["descripcion"],
            activo=activo_asignado,          # Llave foránea a Activo
            sistema_activo=sistema_asignado,        # Llave foránea a Sistema
            componente_activo=componente_asignado,  # Llave foránea a Componente
            usuario=usuario_encargado,        # Instancia de tu modelo usuarios.Usuario
            estado=estado_asignado,
            criticidad=falla_base["criticidad"],
        )
        
        # Sobreescribimos la fecha de creación con el histórico aleatorio
        Solicitud.objects.filter(id=solicitud.id).update(fecha_creacion=fecha_creacion)

        print(f"✅ RQ-{solicitud.id:03d} -> Activo: [{activo_asignado.nombre}] | Sistema: [{sistema_asignado.nombre}] | Componente: [{componente_asignado.nombre}] | Reporta: {usuario_encargado.username}")
        solicitudes_creadas += 1

    print(f"\n🚀 ¡Proceso completado! Se cargaron exitosamente {solicitudes_creadas} solicitudes con datos cruzados en Fixly.")