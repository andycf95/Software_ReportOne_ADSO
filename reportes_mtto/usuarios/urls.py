from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login_usuario, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('lista/', views.lista_usuarios, name='lista_usuarios'),
    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('<int:id>/editar/', views.editar_usuario, name='editar_usuario'),
    path('<int:id>/toggle/', views.toggle_usuario, name='toggle_usuario'),
    path('<int:id>/detalle/', views.detalle_usuario, name='detalle_usuario'),
]