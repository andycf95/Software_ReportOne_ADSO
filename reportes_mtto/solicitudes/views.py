from django.shortcuts import render, get_object_or_404
from .models import Solicitud
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SolicitudForm
from django.shortcuts import redirect
# Create your views here.

#Se crea vista para crear solicitud de mantenimiento

def lista_solicitudes(request):
    solicitudes_list = Solicitud.objects.all().order_by('-id')
    paginator = Paginator(solicitudes_list, 10)
    page = request.GET.get('page', 1)
    try:
        solicitudes = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        solicitudes = paginator.page(1)
    return render(request, 'solicitud_list.html', {'solicitudes': solicitudes})

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
    return render(request, 'solicitud_form.html', {'form': form})

def detalle_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud,id=id)
    return render(request, 'solicitud_detail.html', {'solicitud': solicitud})

def editar_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    form = SolicitudForm(request.POST or None, instance=solicitud)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('solicitudes:lista')
    return render(request, 'solicitud_form.html', {'form': form})

def eliminar_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    if request.method == 'POST':
        solicitud.delete()
    return redirect('solicitudes:lista')
    