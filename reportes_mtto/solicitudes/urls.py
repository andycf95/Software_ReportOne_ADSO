from django.urls import path
from . import views

app_name = 'solicitudes'

urlpatterns = [
    path('', views.lista_solicitudes, name='lista'),
    path('cerradas/', views.lista_solicitudes_cerradas, name='cerradas'),
    path('crear/', views.crear_solicitud, name='crear'),
    path('solicitud/<int:id>/', views.detalle_solicitud, name='solicitud'),
    path('solicitud/<int:id>/cierre/', views.detalle_cierre, name='detalle_cierre'),
    path('solicitud/<int:id>/editar/', views.editar_solicitud, name='editar'),
    path('solicitud/<int:id>/eliminar/', views.eliminar_solicitud, name='eliminar'),
    path('solicitud/<int:id>/cerrar/', views.cerrar_solicitud, name='cerrar'),
    path('solicitud/<int:id>/cambiar-estado-en-proceso/', views.cambiar_estado_en_proceso, name='cambiar_estado_en_proceso'),
]