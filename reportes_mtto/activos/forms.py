from django import forms
from .models import Activo,Sistema,Componente

# Formulario para crear y editar activos, con widgets personalizados para mejorar la experiencia del usuario en el frontend
class ActivoForm(forms.ModelForm):

    class Meta:
        model = Activo
        fields = [
            'nombre',
            'marca',
            'modelo',
            'descripcion',
            'fecha_adquisicion',
            'estado_operativo'
        ]
        
        widgets = {

            'nombre': forms.TextInput(attrs={ 'class': 'form-control'}),
            'marca': forms.TextInput(attrs={ 'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={ 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={ 'class': 'form-control', 'rows': 4}),
            'fecha_adquisicion': forms.DateInput(attrs={ 'class': 'form-control', 'type': 'date'}),
            'estado_operativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Formulario para crear y editar sistemas , con widgets personalizados para mejorar la experiencia del usuario en el frontend
class SistemaForm(forms.ModelForm):
    class Meta:
        model = Sistema
        fields = ['nombre', 'tipo_sistema', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_sistema': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Formulario para crear y editar componentes, con widgets personalizados para mejorar la experiencia del usuario en el frontend
class ComponenteForm(forms.ModelForm):
    class Meta:
        model = Componente
        fields = ['nombre', 'marca', 'modelo', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }