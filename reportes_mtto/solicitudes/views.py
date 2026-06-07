from django.shortcuts import render, get_object_or_404
from .models import Solicitud, Seguimiento
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SolicitudForm
from django.shortcuts import redirect
from django.contrib import messages
from itertools import groupby
from django.utils.timezone import localtime
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied

# Create your views here.

# Función para verificar que el técnico tenga acceso a la solicitud
def verificar_acceso_tecnico(usuario, solicitud):
    if usuario.rol == 'TECNICO':
        if not usuario.activo_asignado or solicitud.activo != usuario.activo_asignado:
            return 'sin_acceso'

#Se crea vista para listar solicitud de mantenimiento activas

@login_required
def lista_solicitudes(request):
    #Los técnicos solo pueden ver las solicitudes cerradas de su activo asignado
    if request.user.rol == 'TECNICO':
        if not request.user.activo_asignado:
            solicitudes_list = Solicitud.objects.none()
        else:
            solicitudes_list = Solicitud.objects.filter(
                activo=request.user.activo_asignado
            ).exclude(estado='CERRADA').order_by('-id')
    else:
        #filtro para mostrar solo solicitudes activas 
        solicitudes_list = Solicitud.objects.select_related('activo').exclude(estado='CERRADA').order_by('-id')

    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()
    criticidad = request.GET.get('criticidad', '').strip()
    fecha_creacion = request.GET.get('fecha_creacion', '').strip()

    #se realiza busqueda por codigo, titulo, descripcion, activo utilizando Q para realizar busqueda en varios campos a la vez
    if q:
        solicitudes_list = solicitudes_list.filter(
            Q(codigo__icontains=q) |
            Q(titulo__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(activo__nombre__icontains=q)
        )
    #se aplican filtros de estado, criticidad y fecha de creación si se proporcionan en la URL
    if estado:
        solicitudes_list = solicitudes_list.filter(estado=estado)

    if criticidad:
        solicitudes_list = solicitudes_list.filter(criticidad=criticidad)

    if fecha_creacion:
        solicitudes_list = solicitudes_list.filter(fecha_creacion__date=fecha_creacion)


    #se aplica paginación a la lista de solicitudes para mostrar 10 por página
    paginator = Paginator(solicitudes_list, 10)
    page = request.GET.get('page', 1)
    
    try:
        solicitudes = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        solicitudes = paginator.page(1)
        
    context = {
        'solicitudes': solicitudes,
        'q': q,
        'estado': estado,
        'criticidad': criticidad,
        'criticidad_choices': Solicitud.CRITICIDAD,
        'fecha_creacion': fecha_creacion,
        "titulo": 'Solicitudes activas',
        'es_cerrada': False,
        'estados_choices': dict(Solicitud.ESTADOS),

    }
    
    return render(request, 'solicitud_list.html', context)

#Se crea vista para listar solicitud de mantenimiento cerradas
@login_required
def lista_solicitudes_cerradas(request):
    #Los técnicos solo pueden ver las solicitudes cerradas de su activo asignado
    if request.user.rol == 'TECNICO':
        if not request.user.activo_asignado:
            solicitudes_list = Solicitud.objects.none()
        else:
            solicitudes_list = Solicitud.objects.filter(
                activo=request.user.activo_asignado,
                estado='CERRADA'
            ).order_by('-fecha_cierre')
    else:
        solicitudes_list = Solicitud.objects.filter(estado='CERRADA').order_by('-fecha_cierre')
        
    #Se obtienen los filtros de búsqueda desde la URL
    q = request.GET.get('q', '').strip()
    criticidad = request.GET.get('criticidad', '').strip()
    fecha_creacion = request.GET.get('fecha_creacion', '').strip()
    fecha_cierre = request.GET.get('fecha_cierre', '').strip()
    
#se realiza busqueda por codigo, titulo, descripcion, activo utilizando Q para realizar busqueda en varios campos a la vez
    if q:
        solicitudes_list = solicitudes_list.filter(
            Q(codigo__icontains=q) |
            Q(titulo__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(activo__nombre__icontains=q)
        )

    if criticidad:
        solicitudes_list = solicitudes_list.filter(criticidad=criticidad)
        
    if fecha_creacion:
        solicitudes_list = solicitudes_list.filter(fecha_creacion__date=fecha_creacion)

    if fecha_cierre:
        solicitudes_list = solicitudes_list.filter(fecha_cierre__date=fecha_cierre)

    paginator = Paginator(solicitudes_list, 10)
    page = request.GET.get('page', 1)
    
    try:
        solicitudes = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        solicitudes = paginator.page(1)
        
    context = {
        'solicitudes': solicitudes,
        'q': q,
        'criticidad': criticidad,
        'criticidad_choices': Solicitud.CRITICIDAD,
        'fecha_cierre': fecha_cierre,
        'fecha_creacion': fecha_creacion,
        "titulo": 'Solicitudes cerradas',
        'es_cerrada': True
    }
    
    return render(request, 'solicitud_list.html', context)

#Se crea vista para crear solicitud de mantenimiento
@login_required
def crear_solicitud(request):
    #Los técnicos deben tener un activo asignado para poder crear solicitudes de mantenimiento, si no tienen un activo asignado se muestra un mensaje de error y se redirige a la lista de solicitudes
    if request.user.rol == 'TECNICO' and not request.user.activo_asignado:
        messages.error(request, 'No tienes un activo asignado. Contacta al administrador.')
        return redirect('solicitudes:lista')
    #Se maneja el formulario de creación de solicitud, asignando el usuario actual como creador y agregando un seguimiento inicial
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            try:
                solicitud = form.save(commit=False) 
                # Validar que el técnico solo cree solicitudes de su activo
                if request.user.rol == 'TECNICO' and solicitud.activo != request.user.activo_asignado:
                    messages.error(request, 'Solo puedes crear solicitudes para tu activo asignado.')
                    return redirect('solicitudes:lista')
                
                solicitud.usuario = request.user 
                solicitud = form.save()
                Seguimiento.objects.create(
                    solicitud=solicitud,
                    usuario=request.user,
                    comentario="Creación de orden|La orden fue creada en estado Pendiente."
                )
                messages.success(request, 'La solicitud se creó correctamente.')
                return redirect('solicitudes:lista')
            except Exception as e:
                messages.error(request, 'Ocurrió un error al crear la solicitud. Intenta de nuevo.')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = SolicitudForm()
    return render(request, 'solicitud_form.html', {'form': form, 'solicitud': None})

#Se crea vista para mostrar detalle de solicitud de mantenimiento
@login_required
def detalle_solicitud(request, id):
    solicitud = get_object_or_404(
        Solicitud.todos.prefetch_related('seguimientos__usuario'), 
        id=id
    )
    verificar_acceso_tecnico(request.user, solicitud)
    seguimientos = solicitud.seguimientos.all().order_by("-fecha")
    seguimientos_preparados = []

#Se preparan los seguimientos para mostrar la fecha, hora, accion y descripcion, separando la accion y descripcion por el caracter "|" en el comentario del seguimientocd
    for seguimiento in seguimientos:
        partes = seguimiento.comentario.split("|", 1)
        if len(partes) == 2:
            accion = partes[0]
            descripcion = partes[1]
        else:
            accion = "Actualización del proceso"
            descripcion = seguimiento.comentario

        seguimientos_preparados.append({
            "fecha": seguimiento.fecha,
            "dia": localtime(seguimiento.fecha).date(),
            "hora": localtime(seguimiento.fecha),
            "accion": accion,
            "descripcion": descripcion,
            "usuario": seguimiento.usuario,
        })

    seguimientos_por_fecha = []

    for dia, items in groupby(seguimientos_preparados, key=lambda s: s["dia"]):
        seguimientos_por_fecha.append({
            "dia": dia,
            "items": list(items)
        })

    context = {
        'solicitud': solicitud,
        'seguimientos_por_fecha': seguimientos_por_fecha,
        'next': request.GET.get('next', '/solicitudes/'),
    }
    return render(request, 'solicitud_detail.html', context)


#Se crea vista para editar solicitud de mantenimiento, detectando cambios de estado y agregando comentarios de seguimiento

@login_required
def editar_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    if verificar_acceso_tecnico(request.user, solicitud) == 'sin_acceso':
        messages.error(request, 'No tienes acceso a esta solicitud.')
        return redirect('solicitudes:lista')
    form = SolicitudForm(request.POST or None, instance=solicitud)
    if request.method == 'POST':
        if solicitud.estado == 'PENDIENTE':
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, 'La solicitud se actualizó correctamente.')
                    return redirect('solicitudes:lista')
                except Exception as e:
                    messages.error(request, 'Ocurrió un error al guardar los cambios.')
            else:
                messages.error(request, 'Por favor corrige los errores del formulario.')
        elif solicitud.estado == 'EN_PROCESO':
            try:
                comentario = request.POST.get('comentario')
                if comentario:
                    Seguimiento.objects.create(
                        solicitud=solicitud,
                        usuario=request.user,
                        comentario=f'Actualización de proceso|{comentario}'
                    )
                    messages.success(request, 'Comentario de seguimiento agregado.')
                return redirect('solicitudes:lista')
            except Exception as e:
                messages.error(request, 'Ocurrió un error al guardar el seguimiento.')

    return render(request, 'solicitud_form.html', {'form': form, 'solicitud': solicitud})


#Se crea vista para boton de cambio de estado de pendiente a en proceso, detectando cambios de estado y agregando comentarios de seguimiento
@require_POST
@login_required
def cambiar_estado_en_proceso(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    if verificar_acceso_tecnico(request.user, solicitud) == 'sin_acceso':
        messages.error(request, 'No tienes acceso a esta solicitud.')
        return redirect('solicitudes:lista')
    try:
        estado_anterior = solicitud.get_estado_display().capitalize()
        solicitud.iniciar_proceso()
        nuevo_estado = solicitud.get_estado_display().capitalize()
        Seguimiento.objects.create(
            solicitud=solicitud,
            usuario=request.user,
            comentario=( f"Cambio de estado|La orden paso de {estado_anterior} a {nuevo_estado}." )
        )
        
        messages.success(request, 'La solicitud entró en proceso correctamente.')
    except ValueError as error:
        messages.error(request, str(error))
        
    return redirect('solicitudes:solicitud', id=solicitud.id)


#Se crea vista para cerrar solicitud de mantenimiento, detectando cambios de estado y agregando comentarios de seguimiento
@login_required
def cerrar_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    if verificar_acceso_tecnico(request.user, solicitud) == 'sin_acceso':
        messages.error(request, 'No tienes acceso a esta solicitud.')
        return redirect('solicitudes:lista')
    # Evita cerrar nuevamente
    if solicitud.estado == 'CERRADA':
        return redirect('solicitudes:solictud', id=solicitud.id)
    
    #Obliga a ingresar el trabajo realizado para cerrar la solicitud
    if request.method == 'POST':
        trabajo_realizado = request.POST.get('trabajo_realizado', '').strip()
        observaciones_cierre = request.POST.get('observaciones_cierre', '').strip()
        
        if not trabajo_realizado:
            return render(request, 'solicitud_cerrar.html', {
                'solicitud': solicitud,
                'error': 'El trabajo realizado es obligatorio.'
            })
        
        try:
            estado_anterior = solicitud.get_estado_display().capitalize()
            solicitud.cerrar(
                trabajo_realizado=trabajo_realizado,
                observaciones_cierre=observaciones_cierre
            )
            nuevo_estado = solicitud.get_estado_display().capitalize()
            # Crear seguimiento automático
            Seguimiento.objects.create(
            solicitud=solicitud,
                usuario=request.user,
                comentario=(
                    f"Cambio de estado|La orden paso de {estado_anterior} a {nuevo_estado}."
                )
            )
            messages.success(request, 'La solicitud se cerró correctamente.')
            return redirect('solicitudes:lista')
        except ValueError as error:
            return render(request, 'solicitud_cerrar.html', {
                'solicitud': solicitud,
                'error': str(error)
            })       

    return render(request,'solicitud_cerrar.html',{'solicitud': solicitud})


#Se crea vista para detalle de cierre de solicitud de mantenimiento
@login_required
def detalle_cierre(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    if verificar_acceso_tecnico(request.user, solicitud) == 'sin_acceso':
        messages.error(request, 'No tienes acceso a esta solicitud.')
        return redirect('solicitudes:lista')
    if solicitud.estado != 'CERRADA':
        return redirect('solicitudes:solicitud', id=solicitud.id)
    return render(request, 'solicitud_cierre_detail.html', {"solicitud": solicitud})

#Se crea vista para eliminar solicitud de mantenimiento
@login_required
@require_POST
def eliminar_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    if verificar_acceso_tecnico(request.user, solicitud) == 'sin_acceso':
        messages.error(request, 'No tienes acceso a esta solicitud.')
        return redirect('solicitudes:lista')
    try:
        solicitud.delete()
        messages.success(request, 'La solicitud fue eliminada correctamente.')
        return redirect('solicitudes:lista')

    except ValidationError as error:
        messages.error(request, error.messages[0])
        return redirect('solicitudes:lista')
    
    
    