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

]
