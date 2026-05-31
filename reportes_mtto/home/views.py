from django.shortcuts import render

#vista para mostrar la página de inicio del sitio web, utilizando una plantilla HTML llamada 'index.html'.
def index(request):
    return render(request, 'home/index.html')

def contacto(request):
    return render(request, 'home/contacto.html')