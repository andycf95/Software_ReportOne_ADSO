from django.forms import ModelForm
from .models import Solicitud
from django import forms

class SolicitudForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['titulo',
            'descripcion',
            'estado',
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

    'estado': forms.Select(attrs={
        'class': 'form-select'
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