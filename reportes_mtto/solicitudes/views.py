from django.shortcuts import render, get_object_or_404
from .models import Solicitud, Seguimiento
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SolicitudForm
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
# Create your views here.

#Se crea vista para listar solicitud de mantenimiento activas

def lista_solicitudes(request):
    solicitudes_list = Solicitud.objects.exclude(estado='CERRADA').order_by('-id')
    paginator = Paginator(solicitudes_list, 10)
    page = request.GET.get('page', 1)
    try:
        solicitudes = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        solicitudes = paginator.page(1)
    return render(request, 'solicitud_list.html', {'solicitudes': solicitudes, "titulo": 'Solicitudes activas'})

#Se crea vista para listar solicitud de mantenimiento cerradas
def lista_solicitudes_cerradas(request):
    solicitudes_list = Solicitud.objects.filter(estado='CERRADA').order_by('-fecha_cierre')
    paginator = Paginator(solicitudes_list, 10)
    page = request.GET.get('page', 1)
    try:
        solicitudes = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        solicitudes = paginator.page(1)
    return render(request, 'solicitud_list.html', {'solicitudes': solicitudes, "titulo": 'Solicitudes cerradas'})

#Se crea vista para crear solicitud de mantenimiento
def crear_solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('solicitudes:lista')
        else:
            print(form.errors)
    else:
        form = SolicitudForm()
    return render(request, 'solicitud_form.html', {'form': form, 'solicitud': None})


#Se crea vista para mostrar detalle de solicitud de mantenimiento
def detalle_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud,id=id)
    return render(request, 'solicitud_detail.html', {'solicitud': solicitud})


#Se crea vista para editar solicitud de mantenimiento, detectando cambios de estado y agregando comentarios de seguimiento
def editar_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    form = SolicitudForm(request.POST or None, instance=solicitud)
    if request.method == 'POST':
        comentario = request.POST.get('comentario')
        if solicitud.estado == 'PENDIENTE':
            if form.is_valid():
                form.save()
                return redirect('solicitudes:lista')
        elif solicitud.estado == 'EN_PROCESO':
            comentario = request.POST.get('comentario')
            if comentario:
                Seguimiento.objects.create(
                    solicitud=solicitud,
                    comentario=f'<strong>Comentario:</strong> {comentario}'
                )
            return redirect('solicitudes:lista')
            
                
    return render(request, 'solicitud_form.html', {'form': form, 'solicitud': solicitud})

#Se crea vista para boton de cambio de estado de pendiente a en proceso, detectando cambios de estado y agregando comentarios de seguimiento
def cambiar_estado_en_proceso(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    if solicitud.estado == 'PENDIENTE':
        estado_anterior = solicitud.get_estado_display().capitalize()
        solicitud.estado = 'EN_PROCESO'
        solicitud.save()
        nuevo_estado = solicitud.get_estado_display().capitalize()
        Seguimiento.objects.create(
            solicitud=solicitud,
            comentario=(
                f'<strong>Estado:</strong> '
                f'{estado_anterior} → {nuevo_estado}<br>'
                f'<strong>Comentario:</strong> '
                f'Cambio automático al iniciar proceso de mantenimiento.'
            )
        )
    return redirect('solicitudes:solicitud', id=solicitud.id)


#Se crea vista para cerrar solicitud de mantenimiento, detectando cambios de estado y agregando comentarios de seguimiento
def cerrar_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)

    # Evita cerrar nuevamente
    if solicitud.estado == 'CERRADA':
        return redirect('solicitudes:detalle', id=solicitud.id)
    if request.method == 'POST':
        trabajo_realizado = request.POST.get('trabajo_realizado', '').strip()
        observaciones_cierre = request.POST.get('observaciones_cierre', '').strip()
        
        if not trabajo_realizado:
            return render(request, 'solicitud_cerrar.html', {
                'solicitud': solicitud,
                'error': 'El trabajo realizado es obligatorio.'
            })
            
        # Actualiza datos de cierre
        solicitud.trabajo_realizado = trabajo_realizado
        solicitud.observaciones_cierre = observaciones_cierre
        solicitud.fecha_cierre = timezone.now()
        solicitud.estado = 'CERRADA'
        solicitud.save()
        # Crear seguimiento automático
        Seguimiento.objects.create(
            solicitud=solicitud,
            comentario=(
                '<strong>Estado:</strong> '
                'En proceso → Cerrada<br>'
                '<strong>Orden cerrada</strong>'
            )
        )
        return redirect('solicitudes:lista')
    return render(request,'solicitud_cerrar.html',{'solicitud': solicitud})


#Se crea vista para detalle de cierre de solicitud de mantenimiento
def detalle_cierre(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    if solicitud.estado != 'CERRADA':
        return redirect('solicitudes:detalle', id=solicitud.id)
    return render(request, 'solicitud_cierre_detail.html', {'solicitud': solicitud})

#Se crea vista para eliminar solicitud de mantenimiento
def eliminar_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    if request.method == 'POST':
        if solicitud.estado != 'PENDIENTE':
            messages.error(
                request,
                'No se puede eliminar una orden en proceso o cerrada.'
            )
            return redirect('solicitudes:lista')
        solicitud.delete()
    return redirect('solicitudes:lista')
    