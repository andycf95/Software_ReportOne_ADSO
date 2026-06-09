from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q

#vista para mostrar la página de inicio del sitio web, utilizando una plantilla HTML llamada 'index.html'.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'home/landing.html')
    
    from solicitudes.models import Solicitud
    from activos.models import Activo
    from django.contrib.auth import get_user_model
    Usuario = get_user_model()

    usuario = request.user
    hoy = timezone.now()
    # Dependiendo del rol del usuario, se generan diferentes estadísticas y se pasan al contexto para renderizar la plantilla.
    if usuario.rol == 'TECNICO':
        activo = usuario.activo_asignado

        if activo:
            solicitudes_activo = Solicitud.objects.filter(activo=activo)
            criticas = solicitudes_activo.filter(criticidad__gte=4).exclude(estado='CERRADA').order_by('-criticidad', 'fecha_creacion')    
        # Calcular días transcurridos para cada solicitud crítica
            for solicitud in criticas:
                solicitud.dias_transcurridos = (timezone.now() - solicitud.fecha_creacion).days
            context = {
                'pendientes': solicitudes_activo.filter(estado='PENDIENTE').count(),
                'en_proceso': solicitudes_activo.filter(estado='EN_PROCESO').count(),
                'recientes': solicitudes_activo.exclude(estado='CERRADA').order_by('-fecha_creacion')[:5],
                'criticas': solicitudes_activo.filter(
                    criticidad__gte=4
                ).exclude(estado='CERRADA').order_by('-criticidad', 'fecha_creacion'),
                'activo': activo,
                'criticas': criticas,
            }
        else:
            context = {
                'pendientes': 0,
                'en_proceso': 0,
                'recientes': [],
                'criticas': [],
                'activo': None,
                
            }

    elif usuario.rol == 'SUPERVISOR':
        solicitudes_activas = Solicitud.objects.exclude(estado='CERRADA')
        criticas = Solicitud.objects.filter(criticidad__gte=4).exclude(estado='CERRADA').order_by('-criticidad','fecha_creacion')
        por_estado = [
                {'estado': 'Pendiente', 'total': Solicitud.objects.filter(estado='PENDIENTE').count()},
                {'estado': 'En proceso', 'total': Solicitud.objects.filter(estado='EN_PROCESO').count()},
            ]

        # Calcular porcentajes para la gráfica de estados
        total = por_estado[0]['total'] + por_estado[1]['total']
        pendientes_pct = round(por_estado[0]['total'] / total * 100) if total > 0 else 0
        en_proceso_pct = round(por_estado[1]['total'] / total * 100) if total > 0 else 0
        
        for solicitud in criticas:
            solicitud.dias_transcurridos = (timezone.now() - solicitud.fecha_creacion).days
        context = {
            'total_solicitudes_activas': solicitudes_activas.count(),
            'activos_con_solicitudes': Solicitud.objects.exclude(
                estado='CERRADA'
            ).values('activo').distinct().count(),
            'top_activos': Solicitud.objects.exclude(estado='CERRADA').values(
                'activo__nombre'
            ).annotate(total=Count('id')).order_by('-total')[:5],
            'antiguedad_30': solicitudes_activas.filter(
                fecha_creacion__lte=hoy - timedelta(days=30)
            ).count(),
            'antiguedad_60': solicitudes_activas.filter(
                fecha_creacion__lte=hoy - timedelta(days=60)
            ).count(),
            'antiguedad_90': solicitudes_activas.filter(
                fecha_creacion__lte=hoy - timedelta(days=90)
            ).count(),
            'criticas': criticas,
            'por_estado': por_estado,
            'pendientes_pct': pendientes_pct,
            'en_proceso_pct': en_proceso_pct,
        }

    else:  # ADMIN
        solicitudes_activas = Solicitud.objects.exclude(estado='CERRADA')
        por_estado = [
                {'estado': 'Pendiente', 'total': Solicitud.objects.filter(estado='PENDIENTE').count()},
                {'estado': 'En proceso', 'total': Solicitud.objects.filter(estado='EN_PROCESO').count()},
            ]

        # Calcular porcentajes para la gráfica de estados
        total = por_estado[0]['total'] + por_estado[1]['total']
        pendientes_pct = round(por_estado[0]['total'] / total * 100) if total > 0 else 0
        en_proceso_pct = round(por_estado[1]['total'] / total * 100) if total > 0 else 0
        
        # Obtener solicitudes críticas (criticidad >= 4) que no estén cerradas, ordenadas por criticidad y fecha de creación
        criticas = Solicitud.objects.filter(criticidad__gte=4).exclude(estado='CERRADA').order_by('-criticidad','fecha_creacion')

        for solicitud in criticas:
            solicitud.dias_transcurridos = (timezone.now() - solicitud.fecha_creacion).days
            
        context = {
            'total_solicitudes_activas': solicitudes_activas.count(),
            'total_activos': Activo.objects.count(),
            'total_usuarios_activos': Usuario.objects.filter(is_active=True).count(),
            'cerradas_mes': Solicitud.objects.filter(
                estado='CERRADA',
                fecha_cierre__month=hoy.month,
                fecha_cierre__year=hoy.year
            ).count(),
            'por_estado': por_estado,
            'pendientes_pct': pendientes_pct,
            'en_proceso_pct': en_proceso_pct,
            'antiguedad_30': solicitudes_activas.filter(
                fecha_creacion__lte=hoy - timedelta(days=30)
            ).count(),
            'antiguedad_60': solicitudes_activas.filter(
                fecha_creacion__lte=hoy - timedelta(days=60)
            ).count(),
            'antiguedad_90': solicitudes_activas.filter(
                fecha_creacion__lte=hoy - timedelta(days=90)
            ).count(),
            'criticas': Solicitud.objects.filter(
                criticidad__gte=4
            ).exclude(estado='CERRADA').select_related('activo').order_by('-criticidad', '-fecha_creacion'),
            'top_activos': Solicitud.objects.exclude(estado='CERRADA').values(
                'activo__nombre'
            ).annotate(total=Count('id')).order_by('-total')[:5],
            'top_usuarios': Solicitud.objects.filter(
                fecha_creacion__month=hoy.month,
                fecha_creacion__year=hoy.year
            ).values(
                'usuario__first_name', 'usuario__last_name', 'usuario__username'
            ).annotate(total=Count('id')).order_by('-total')[:5],
            'criticas': criticas,
        }

    context['rol'] = usuario.rol
    return render(request, 'home/index.html', context)

def contacto(request):
    return render(request, 'home/contacto.html')