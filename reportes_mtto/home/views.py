from django.shortcuts import render

#vista para mostrar la página de inicio del sitio web, utilizando una plantilla HTML llamada 'index.html'.
def index(request):
    if request.user.is_authenticated:
        return render(request, 'home/index.html')  # dashboard para usuarios con sesión
    return render(request, 'home/landing.html')    # landing para usuarios sin sesión

def contacto(request):
    return render(request, 'home/contacto.html')