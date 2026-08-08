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
            'componente_activo',]
        
        widgets = {

            'titulo': forms.TextInput(attrs={ 
                                                'class': 'form-control',
                                                'minlength': '15',
                                                'maxlength': '150',
                                                'placeholder': 'Mínimo 15 caracteres — describe la falla y su ubicación...',
                                             }),
            'descripcion': forms.Textarea(attrs={ 
                                                'class': 'form-control', 
                                                'rows': 4,
                                                'minlength': '30',
                                                'placeholder': 'Mínimo 30 caracteres — describe la falla y su ubicación...'
                                                }),
            'criticidad': forms.Select(attrs={'class': 'form-select'}),
            "activo": forms.Select(attrs={"id": "id_activo", "class": "form-select"}),
            "sistema_activo": forms.Select(attrs={"id": "id_sistema", "class": "form-select"}),
            "componente_activo": forms.Select(attrs={"id": "id_componente", "class": "form-select"}),
        }
        
        
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo', '').strip()
        if len(titulo) < 15:
            raise forms.ValidationError(
                "El título debe tener al menos 15 caracteres. "
                "Describe la falla y su ubicación."
            )
        return titulo

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion', '').strip()
        if len(descripcion) < 30:
            raise forms.ValidationError(
                "La descripción debe tener al menos 30 caracteres. "
                "Incluye los síntomas, cuándo ocurrió y el impacto en la operación."
            )
        return descripcion   
        
    # Este método se ejecuta cada vez que se crea una instancia del formulario, ya sea para crear una nueva solicitud o para editar una existente.
    # Aquí es donde configuramos la lógica para cargar dinámicamente los sistemas y subsistemas relacionados con el activo seleccionado, y también para deshabilitar los campos si la solicitud no está en estado "PENDIENTE".
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from activos.models import Activo, Sistema, Componente
        if self.instance and self.instance.estado != 'PENDIENTE':
            for field in self.fields.values():
                field.widget.attrs['disabled'] = True
        
        #Esto es para mostrar un mensaje por defecto en los dropdowns de activos, sistemas y componentes, indicando al usuario que debe seleccionar una opción. También inicializamos los querysets de sistemas y componentes como vacíos para evitar que se muestren opciones no relacionadas al cargar el formulario por primera vez.
        self.fields['activo'].empty_label = "Seleccione un activo..."
        self.fields['sistema_activo'].empty_label = "Seleccione un sistema..."
        self.fields['componente_activo'].empty_label = "Seleccione un componente..."
        
        self.fields['sistema_activo'].queryset = Sistema.objects.none()
        self.fields['componente_activo'].queryset = Componente.objects.none()
        
        if 'activo' in self.data:
            try:
                activo_id = int(self.data.get('activo'))
                
                self.fields['sistema_activo'].queryset = Sistema.objects.filter(activo_id=activo_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        
        elif self.instance.pk and self.instance.activo:
            self.fields['sistema_activo'].queryset = Sistema.objects.filter(activo=self.instance.activo).order_by('nombre')

        
        if 'sistema_activo' in self.data:
            try:
                sistema_id = int(self.data.get('sistema_activo'))
                self.fields['componente_activo'].queryset = Componente.objects.filter(sistema_id=sistema_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.sistema_activo:
            self.fields['componente_activo'].queryset = Componente.objects.filter(sistema=self.instance.sistema_activo).order_by('nombre')
