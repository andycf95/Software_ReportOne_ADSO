from django.urls import path
from . import views

app_name = 'activos' 

urlpatterns = [

    path('', views.lista_activos_jerarquia, name='lista_activos'),
    path('activo/<int:id>/detalle/', views.detalle_activo, name='detalle_activo'),
    path('sistema/<int:id>/detalle/', views.detalle_sistema,name='detalle_sistema'),
    path('subsistema/<int:id>/detalle/', views.detalle_subsistema,name='detalle_subsistema'),
    path(  "ajax/sistemas/", views.obtener_sistemas, name="obtener_sistemas"),
    path( "ajax/subsistemas/", views.obtener_subsistemas, name="obtener_subsistemas"),

]
