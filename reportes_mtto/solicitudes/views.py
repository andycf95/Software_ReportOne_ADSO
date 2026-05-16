from django.shortcuts import render
from .models import Solicitud
# Create your views here.
def create_solicitud(request):
    return render(request, 'solicitud_form.html')