from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login_usuario, name='login'), # Usamos la vista personalizada para manejar el login
    path('logout/', LogoutView.as_view(), name='logout'), # Usamos la vista genérica de Django para logout
    path('perfil/', views.perfil_usuario, name='perfil'), # Vista para mostrar el perfil del usuario con estadísticas de sus solicitudes
    path('lista/', views.lista_usuarios, name='lista_usuarios'), # Vista para listar usuarios con filtros y paginación
    path('crear/', views.crear_usuario, name='crear_usuario'), # Vista para crear un nuevo usuario (solo para administradores)
    path('<int:id>/editar/', views.editar_usuario, name='editar_usuario'), # Vista para editar un usuario existente (solo para administradores)
    path('<int:id>/toggle/', views.toggle_usuario, name='toggle_usuario'), # Vista para activar/desactivar un usuario (solo para administradores)
    path('<int:id>/detalle/', views.detalle_usuario, name='detalle_usuario'), # Vista para mostrar el detalle de un usuario y sus solicitudes recientes (solo para administradores)
    path('<int:id>/asignar-activo/', views.asignar_activo, name='asignar_activo'),# Vista para asignar o desasignar un activo a un técnico (solo para administradores)
    path('<int:id>/cambiar-contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'), # Vista para cambiar la contraseña de un usuario (solo para administradores)
]   