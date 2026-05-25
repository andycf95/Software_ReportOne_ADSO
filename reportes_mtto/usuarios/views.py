from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login


from .forms import RegistroUsuarioForm


# Create your views here.
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso. ¡Bienvenido!')
            return redirect('usuarios:login')
    else:
        form = RegistroUsuarioForm()
        
    contexto = {
        'form': form
    }
    return render(request, 'registro.html', contexto)

def perfil_usuario(request):
    return render(request, 'perfil.html')
