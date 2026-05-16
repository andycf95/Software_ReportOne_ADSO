from django.urls import path
from . import views

app_name = 'solicitudes'

urlpatterns = [
    path('crear/', views.create_solicitud, name='create'),
]