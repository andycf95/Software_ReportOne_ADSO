from django.shortcuts import render
from .models import Activo, Sistema, Componente
from solicitudes.models import Solicitud
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import ActivoForm
from django.views.decorators.http import require_POST
from .forms import ActivoForm, SistemaForm, ComponenteForm
import json
from django.db.models import ProtectedError
from django.contrib import messages

#Vista para mostrar la jerarquía de activos, sistemas y componentes en una sola página, utilizando prefetch_related para optimizar las consultas a la base de datos y evitar el problema de N+1 consultas.
@login_required
def lista_activos_jerarquia(request):
    
    activos = Activo.objects.prefetch_related('sistemas__componentes').all()
    
    contexto = {
        'activos': activos
    }
    
    return render(request, 'activos_list.html', contexto)

#Vista para crear un nuevo activo, utilizando un formulario basado en el modelo ActivoForm.
# Si el formulario es válido, se guarda el nuevo activo y se redirige a la lista de activos.
@login_required
def crear_activo(request):
    if request.method == 'POST':
        form = ActivoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('activos:lista_activos')
    else:
        form = ActivoForm()
    return render(request, 'form_activo.html', {
        'form': form,
        'titulo': 'Nuevo Activo',
        'btn_texto': 'Guardar'
    })


@login_required
def editar_activo(request, id):
    activo = get_object_or_404(Activo, id=id)
    if request.method == 'POST':
        form = ActivoForm(request.POST, instance=activo)
        if form.is_valid():
            form.save()
            return redirect('activos:lista_activos')
    else:
        form = ActivoForm(instance=activo)
    return render(request, 'form_activo.html', {
        'form': form,
        'titulo': f'Editar Activo — {activo.nombre}',
        'btn_texto': 'Actualizar'
    })

@login_required
def crear_sistema(request, activo_id):
    activo = get_object_or_404(Activo, id=activo_id)
    if request.method == 'POST':
        form = SistemaForm(request.POST)
        if form.is_valid():
            sistema = form.save(commit=False)
            sistema.activo = activo
            sistema.save()
            return redirect('activos:lista_activos')
    else:
        form = SistemaForm()
    return render(request, 'form_sistema.html', {
        'form': form,
        'activo': activo,
        'titulo': f'Nuevo Sistema — {activo.nombre}',
        'btn_texto': 'Guardar',
        'activo_padre': activo.nombre,
    })


@login_required
def editar_sistema(request, id):
    sistema = get_object_or_404(Sistema, id=id)
    if request.method == 'POST':
        form = SistemaForm(request.POST, instance=sistema)
        if form.is_valid():
            form.save()
            return redirect('activos:lista_activos')
    else:
        form = SistemaForm(instance=sistema)
    return render(request, 'form_sistema.html', {
        'form': form,
        'titulo': f'Editar Sistema — {sistema.nombre}',
        'btn_texto': 'Actualizar',
        'activo_padre': sistema.activo.nombre,
    })


@login_required
def crear_componente(request, sistema_id):
    sistema = get_object_or_404(Sistema, id=sistema_id)
    if request.method == 'POST':
        form = ComponenteForm(request.POST)
        if form.is_valid():
            componente = form.save(commit=False)
            componente.sistema = sistema
            componente.save()
            return redirect('activos:lista_activos')
    else:
        form = ComponenteForm()
    return render(request, 'form_componente.html', {
        'form': form,
        'sistema': sistema,
        'titulo': f'Nuevo Componente — {sistema.nombre}',
        'btn_texto': 'Guardar',
        'activo_padre': sistema.activo.nombre,
        'sistema_padre': sistema.nombre,
    })


@login_required
def editar_componente(request, id):
    componente = get_object_or_404(Componente, id=id)
    if request.method == 'POST':
        form = ComponenteForm(request.POST, instance=componente)
        if form.is_valid():
            form.save()
            return redirect('activos:lista_activos')
    else:
        form = ComponenteForm(instance=componente)
    return render(request, 'form_componente.html', {
        'form': form,
        'titulo': f'Editar Componente — {componente.nombre}',
        'btn_texto': 'Actualizar',
        'activo_padre': componente.sistema.activo.nombre,
        'sistema_padre': componente.sistema.nombre,
    })
    
#Vista para mostrar los detalles de un activo específico en formato JSON, incluyendo su nombre, código, marca, modelo, 
#fecha de adquisición, estado operativo y una descripción. Si el activo no tiene marca o modelo, se muestra un guion como valor predeterminado.
def detalle_activo(request, id):
    activo = get_object_or_404(Activo, id=id)
    total_solicitudes = Solicitud.objects.filter(activo=activo).exclude(estado='CERRADA').count()

    return JsonResponse({
        "id": activo.id,
        "tipo": "Activo",
        "nombre": activo.nombre,
        "codigo": activo.codigo,
        "marca": activo.marca or "-",
        "modelo": activo.modelo or "-",
        "fecha": activo.fecha_adquisicion.strftime("%d/%m/%Y") if activo.fecha_adquisicion else "-",
        "activo_padre": "-",
        "sistema_padre": "-",
        "descripcion": activo.descripcion or "-",
        "estado": "Activo" if activo.estado_operativo else "Fuera de servicio",
        "icono": "bi-ship",
        "color": "#d1fae5",
        "texto": "#065f46",
        'total_solicitudes': total_solicitudes
    })
    

#Vista para mostrar los detalles de un sistema específico en formato JSON, incluyendo su nombre, código, tipo de sistema, 
# descripción y el nombre del activo al que está asociado. Si el sistema no tiene descripción, 
# se muestra un guion como valor predeterminado.
def detalle_sistema(request, id):
    sistema = get_object_or_404(Sistema, id=id)

    return JsonResponse({
        "id": sistema.id,
        "tipo": "Sistema",
        "nombre": sistema.nombre,
        "codigo": f"SIS-{sistema.id}",
        "marca": "-",
        "modelo": "-",
        "fecha": "-",
        "activo_padre": sistema.activo.nombre,
        "sistema_padre": "-",
        "descripcion": sistema.descripcion or "-",
        "estado": "-",
        "icono": "bi-gear-fill",
        "color": "#e0e7ff",
        "texto": "#3730a3",
    })

#Vista para mostrar los detalles de un componente específico en formato JSON, incluyendo su nombre, código,
# marca, modelo, descripción y el nombre del sistema y activo a los que está asociado. 
# Si el componente no tiene marca o modelo, se muestra un guion como valor predeterminado.
def detalle_componente(request, id):
    componente = get_object_or_404(Componente, id=id)

    return JsonResponse({
        "id": componente.id,
        "tipo": "Componente",
        "nombre": componente.nombre,
        "codigo": f"COMP-{componente.id}",
        "marca": componente.marca or "-",
        "modelo": componente.modelo or "-",
        "fecha": "-",
        "activo_padre": componente.sistema.activo.nombre,
        "sistema_padre": componente.sistema.nombre,
        "descripcion": componente.descripcion or "-",
        "estado": "-",
        "icono": "bi-nut",
        "color": "#eff6ff",
        "texto": "#1d4ed8",
    })
    

#Vista para obtener los sistemas asociados a un activo específico, 
# utilizando el ID del activo pasado como parámetro en la solicitud GET. 
# La respuesta se devuelve en formato JSON con una lista de sistemas que incluyen su ID y nombre.
def obtener_sistemas(request):

    activo_id = request.GET.get("activo_id")

    sistemas = Sistema.objects.filter( activo_id=activo_id ).values("id", "nombre")

    return JsonResponse(list(sistemas),safe=False)

#Vista para obtener los componentes asociados a un sistema específico, 
# utilizando el ID del sistema pasado como parámetro en la solicitud GET. 
# La respuesta se devuelve en formato JSON con una lista de componentes que incluyen su ID y nombre.
def obtener_componentes(request):

    sistema_id = request.GET.get("sistema_id")

    componentes = Componente.objects.filter( sistema_id=sistema_id).values(
        "id",
        "nombre"
    )

    return JsonResponse(list(componentes),safe=False)

@login_required
def eliminar_activo(request, id):
    activo = get_object_or_404(Activo, id=id)
    if request.method == 'POST':
        try:
            activo.delete()
            messages.success(request, f'Activo "{activo.nombre}" eliminado correctamente.')
        except ProtectedError:
            messages.error(request, f'No se puede eliminar "{activo.nombre}" porque tiene solicitudes de mantenimiento asociadas.')
    return redirect('activos:lista_activos')


@login_required
def eliminar_sistema(request, id):
    sistema = get_object_or_404(Sistema, id=id)
    if request.method == 'POST':
        try:
            sistema.delete()
            messages.success(request, f'Sistema "{sistema.nombre}" eliminado correctamente.')
        except ProtectedError:
            messages.error(request, f'No se puede eliminar "{sistema.nombre}" porque tiene solicitudes de mantenimiento asociadas.')
    return redirect('activos:lista_activos')


@login_required
def eliminar_componente(request, id):
    componente = get_object_or_404(Componente, id=id)
    if request.method == 'POST':
        try:
            componente.delete()
            messages.success(request, f'Componente "{componente.nombre}" eliminado correctamente.')
        except ProtectedError:
            messages.error(request, f'No se puede eliminar "{componente.nombre}" porque tiene solicitudes de mantenimiento asociadas.')
    return redirect('activos:lista_activos')
    componente = get_object_or_404(Componente, id=id)
    if request.method == 'POST':
        componente.delete()
        return redirect('activos:lista_activos')
    return redirect('activos:lista_activos')