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

            'titulo': forms.TextInput(attrs={ 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={ 'class': 'form-control', 'rows': 4}),
            'criticidad': forms.Select(attrs={'class': 'form-select'}),
            "activo": forms.Select(attrs={"id": "id_activo", "class": "form-select"}),
            "sistema_activo": forms.Select(attrs={"id": "id_sistema", "class": "form-select"}),
            "subsistema_activo": forms.Select(attrs={"id": "id_subsistema", "class": "form-select"}),
        }
        
    # Este método se ejecuta cada vez que se crea una instancia del formulario, ya sea para crear una nueva solicitud o para editar una existente.
    # Aquí es donde configuramos la lógica para cargar dinámicamente los sistemas y subsistemas relacionados con el activo seleccionado, y también para deshabilitar los campos si la solicitud no está en estado "PENDIENTE".
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from activos.models import Activo, Sistema, SubSistema
        if self.instance and self.instance.estado != 'PENDIENTE':
            for field in self.fields.values():
                field.widget.attrs['disabled'] = True
                
        self.fields['activo'].empty_label = "Seleccione un activo..."
        self.fields['sistema_activo'].empty_label = "Seleccione un sistema..."
        self.fields['subsistema_activo'].empty_label = "Seleccione un subsistema..."
        
        self.fields['sistema_activo'].queryset = Sistema.objects.none()
        self.fields['subsistema_activo'].queryset = SubSistema.objects.none()
        
        if 'activo' in self.data:
            try:
                activo_id = int(self.data.get('activo'))
                # Llenamos el queryset solo con los sistemas de ese activo
                self.fields['sistema_activo'].queryset = Sistema.objects.filter(activo_id=activo_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        #  esto cargará los datos guardados
        elif self.instance.pk and self.instance.activo:
            self.fields['sistema_activo'].queryset = Sistema.objects.filter(activo=self.instance.activo).order_by('nombre')

        #  Hacemos exactamente lo mismo para el nivel de subsistemas
        if 'sistema_activo' in self.data:
            try:
                sistema_id = int(self.data.get('sistema_activo'))
                self.fields['subsistema_activo'].queryset = SubSistema.objects.filter(sistema_id=sistema_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.sistema_activo:
            self.fields['subsistema_activo'].queryset = SubSistema.objects.filter(sistema=self.instance.sistema_activo).order_by('nombre')
