from django.urls import path
from . import views

app_name = 'solicitudes'

urlpatterns = [
    path('', views.lista_solicitudes, name='lista'), # Vista para listar solicitudes abiertas con filtros y paginación
    path('cerradas/', views.lista_solicitudes_cerradas, name='cerradas'), # Vista para listar solicitudes cerradas con filtros y paginación
    path('crear/', views.crear_solicitud, name='crear'), # Vista para crear una nueva solicitud (accesible para técnicos y supervisores)
    path('solicitud/<int:id>/', views.detalle_solicitud, name='solicitud'), # Vista para mostrar el detalle de una solicitud específica, incluyendo su historial de cambios y comentarios
    path('solicitud/<int:id>/cierre/', views.detalle_cierre, name='detalle_cierre'), # Vista para mostrar el detalle del cierre de una solicitud, incluyendo la causa de cierre y la evaluación del técnico
    path('solicitud/<int:id>/editar/', views.editar_solicitud, name='editar'), # Vista para editar una solicitud existente (accesible para técnicos y supervisores, pero solo si la solicitud no está cerrada)
    path('solicitud/<int:id>/eliminar/', views.eliminar_solicitud, name='eliminar'), # Vista para eliminar una solicitud (accesible solo para supervisores, y solo si la solicitud no está cerrada)
    path('solicitud/<int:id>/cerrar/', views.cerrar_solicitud, name='cerrar'), # Vista para cerrar una solicitud (accesible solo para supervisores, y solo si la solicitud no está cerrada)
    path('solicitud/<int:id>/cambiar-estado-en-proceso/', views.cambiar_estado_en_proceso, name='cambiar_estado_en_proceso'), # Vista para cambiar el estado de una solicitud a "En Proceso" (accesible solo para técnicos, y solo si la solicitud está en estado "Pendiente")
]