from django.forms import ModelForm
from .models import Solicitud
from django import forms

class SolicitudForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['titulo',
            'descripcion',
            'criticidad',
            'activo',
            'sistema_activo',
            'subsistema_activo',]
        
        widgets = {

            'titulo': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),


            'criticidad': forms.Select(attrs={
                'class': 'form-select'
            }),

            'activo': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'sistema_activo': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'subsistema_activo': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.estado != 'PENDIENTE':
            for field in self.fields.values():
                field.widget.attrs['disabled'] = True