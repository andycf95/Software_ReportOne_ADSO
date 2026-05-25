from django.shortcuts import render

# Create your views here.
def registro_usuario(request):
    return render(request, 'registro.html')
