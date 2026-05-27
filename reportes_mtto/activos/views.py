from django.shortcuts import render
from .models import Activo, Sistema, SubSistema
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def lista_activos_jerarquia(request):
    
    activos = Activo.objects.prefetch_related('sistemas__subsistemas').all()
    
    contexto = {
        'activos': activos
    }
    
    return render(request, 'activos_list.html', contexto)






def detalle_activo(request, id):
    activo = get_object_or_404(Activo, id=id)

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
    })
    

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
        "estado": "Activo",
        "icono": "bi-gear-fill",
        "color": "#e0e7ff",
        "texto": "#3730a3",
    })


def detalle_subsistema(request, id):
    subsistema = get_object_or_404(SubSistema, id=id)

    return JsonResponse({
        "id": subsistema.id,
        "tipo": "Subsistema",
        "nombre": subsistema.nombre,
        "codigo": f"SUB-{subsistema.id}",
        "marca": "-",
        "modelo": "-",
        "fecha": "-",
        "activo_padre": subsistema.sistema.activo.nombre,
        "sistema_padre": subsistema.sistema.nombre,
        "descripcion": subsistema.descripcion or "-",
        "estado": "Activo",
        "icono": "bi-nut",
        "color": "#eff6ff",
        "texto": "#1d4ed8",
    })
    

def obtener_sistemas(request):

    activo_id = request.GET.get("activo_id")

    sistemas = Sistema.objects.filter( activo_id=activo_id ).values("id", "nombre")

    return JsonResponse(list(sistemas),safe=False)


def obtener_subsistemas(request):

    sistema_id = request.GET.get("sistema_id")

    subsistemas = SubSistema.objects.filter( sistema_id=sistema_id).values(
        "id",
        "nombre"
    )

    return JsonResponse(list(subsistemas),safe=False)

