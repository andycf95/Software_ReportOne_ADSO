from django.urls import path
from . import views

app_name = 'activos' 

urlpatterns = [

    path('', views.lista_activos_jerarquia, name='lista_activos'), # Vista para listar activos con filtros y paginación, mostrando la jerarquía de sistemas y componentes
    path('activo/<int:id>/detalle/', views.detalle_activo, name='detalle_activo'), # Vista para mostrar el detalle de un activo específico, incluyendo su historial de mantenimiento y solicitudes asociadas
    path('sistema/<int:id>/detalle/', views.detalle_sistema,name='detalle_sistema'), # Vistas para mostrar el detalle de un sistema o componente específico, incluyendo su historial de mantenimiento y solicitudes asociadas
    path('componente/<int:id>/detalle/', views.detalle_componente,name='detalle_componente'), # Vistas para mostrar el detalle de un sistema o componente específico, incluyendo su historial de mantenimiento y solicitudes asociadas
    path(  "ajax/sistemas/", views.obtener_sistemas, name="obtener_sistemas"), # Vistas para manejar las solicitudes AJAX
    path( "ajax/componentes/", views.obtener_componentes, name="obtener_componentes"), # Vistas para manejar las solicitudes AJAX 
    path('crear/', views.crear_activo, name='crear_activo'), # Vista para crear un nuevo activo
    path('sistema/<int:activo_id>/nuevo/', views.crear_sistema, name='crear_sistema'), # Vista para crear un nuevo sistema asociado a un activo específico
    path('componente/<int:sistema_id>/nuevo/', views.crear_componente, name='crear_componente'), # Vista para crear un nuevo componente asociado a un sistema específico
    path('activo/<int:id>/eliminar/', views.eliminar_activo, name='eliminar_activo'), # Vista para eliminar un activo específico, 
    path('sistema/<int:id>/eliminar/', views.eliminar_sistema, name='eliminar_sistema'), # Vistas para eliminar un sistema 
    path('activo/<int:id>/editar/', views.editar_activo, name='editar_activo'), # Vista para editar un activo específico
    path('sistema/<int:id>/editar/', views.editar_sistema, name='editar_sistema'), # Vistas para editar un sistema 
    path('componente/<int:id>/editar/', views.editar_componente, name='editar_componente'), # Vistas para editar un componente específico
]
