from django.forms import ModelForm
from .models import Solicitud

class SolicitudForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['titulo',
            'descripcion',
            'criticidad',
            'activo',
            'sistema_activo',
            'subsistema_activo',]