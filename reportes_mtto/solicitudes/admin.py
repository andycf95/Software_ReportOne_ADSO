from django.contrib import admin
from .models import Solicitud
from .models import Seguimiento

# Register your models here.
admin.site.register(Solicitud)
admin.site.register(Seguimiento)
