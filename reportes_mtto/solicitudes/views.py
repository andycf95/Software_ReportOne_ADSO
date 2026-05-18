from django.shortcuts import render, get_object_or_404
from .models import Solicitud, Seguimiento
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SolicitudForm
from django.shortcuts import redirect
# Create your views here.

#Se crea vista para listar solicitud de mantenimiento

def lista_solicitudes(request):
    solicitudes_list = Solicitud.objects.all().order_by('-id')
    paginator = Paginator(solicitudes_list, 10)
    page = request.GET.get('page', 1)
    try:
        solicitudes = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        solicitudes = paginator.page(1)
    return render(request, 'solicitud_list.html', {'solicitudes': solicitudes})

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
    estado_anterior = solicitud.get_estado_display().capitalize() # Obtener la representación legible del estado antes de la actualización
    form = SolicitudForm(request.POST or None, instance=solicitud)
    if request.method == 'POST' and form.is_valid():
        solicitud_actualizada = form.save()
        comentario = request.POST.get('comentario')
        nuevo_estado = solicitud_actualizada.get_estado_display().capitalize()  # Obtener la representación legible del estado
        texto_seguimiento = ''

        # Detectar cambio de estado
        if estado_anterior != nuevo_estado:

            texto_seguimiento += (
                f'<strong>Estado:</strong> '
                f'{estado_anterior} → {nuevo_estado}<br><br>'
            )
            
        #Comentario manual
        if comentario:

            texto_seguimiento += (
                f'<strong>Comentario:</strong> '
                f'{comentario} '
            )
            
        #Crea un solo comentario de seguimiento si hay cambios de estado o comentario manual
        if texto_seguimiento:
            Seguimiento.objects.create(
                solicitud=solicitud,
                comentario=texto_seguimiento
            )
        return redirect('solicitudes:lista')
    return render(request, 'solicitud_form.html', {'form': form, 'solicitud': solicitud})

#Se crea vista para eliminar solicitud de mantenimiento
def eliminar_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    if request.method == 'POST':
        solicitud.delete()
    return redirect('solicitudes:lista')
    