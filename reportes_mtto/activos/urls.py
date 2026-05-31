from django.urls import path
from . import views

app_name = 'activos' 

urlpatterns = [

    path('', views.lista_activos_jerarquia, name='lista_activos'),
    path('activo/<int:id>/detalle/', views.detalle_activo, name='detalle_activo'),
    path('sistema/<int:id>/detalle/', views.detalle_sistema,name='detalle_sistema'),
    path('componente/<int:id>/detalle/', views.detalle_componente,name='detalle_componente'),
    path(  "ajax/sistemas/", views.obtener_sistemas, name="obtener_sistemas"),
    path( "ajax/componentes/", views.obtener_componentes, name="obtener_componentes"),
    path('crear/', views.crear_activo, name='crear_activo'),
    path('sistema/<int:activo_id>/nuevo/', views.crear_sistema, name='crear_sistema'),
    path('componente/<int:sistema_id>/nuevo/', views.crear_componente, name='crear_componente'),
    path('activo/<int:id>/eliminar/', views.eliminar_activo, name='eliminar_activo'),
    path('sistema/<int:id>/eliminar/', views.eliminar_sistema, name='eliminar_sistema'),
    path('componente/<int:id>/eliminar/', views.eliminar_componente, name='eliminar_componente'),
    path('activo/<int:id>/editar/', views.editar_activo, name='editar_activo'),
    path('sistema/<int:id>/editar/', views.editar_sistema, name='editar_sistema'),
    path('componente/<int:id>/editar/', views.editar_componente, name='editar_componente'),
]
