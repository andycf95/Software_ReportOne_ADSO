from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'usuarios'

urlpatterns = [
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil'),
]