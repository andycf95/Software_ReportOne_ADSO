from django import forms
from django.contrib.auth import get_user_model

Usuario = get_user_model()

# Formulario para registro de usuario
class UsuarioAdminForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email',
                  'numero_identificacion', 'telefono', 'rol']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'numero_identificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['password1']) #sirve para encriptar la contraseña
        if commit:
            usuario.save()
        return usuario
    
# Formulario para editar usuario (sin contraseña)
class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email',
                  'numero_identificacion', 'telefono', 'rol', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'numero_identificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
