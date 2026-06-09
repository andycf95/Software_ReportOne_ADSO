from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import  UsuarioAdminForm, EditarUsuarioForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from activos.models import Activo
from django.http import JsonResponse

# Create your views here.
Usuario = get_user_model()


# ─── VISTAS DE AUTENTICACIÓN Y PERFIL ───
def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Verificar si el usuario existe pero está inactivo
        try:
            usuario = Usuario.objects.get(username=username)
            if not usuario.is_active:
                messages.error(request, 'Tu cuenta se encuentra desactivada. Contacta al administrador.')
                return render(request, 'login.html', {'form': form})
        except Usuario.DoesNotExist:
            pass

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home:index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

#vista para mostrar el perfil del usuario con estadísticas de sus solicitudes
@login_required
def perfil_usuario(request):
    from solicitudes.models import Solicitud
    usuario = request.user
    if usuario.rol == 'TECNICO':
        if usuario.activo_asignado:
            total = Solicitud.objects.filter(activo=usuario.activo_asignado)
        else:
            total = Solicitud.objects.none()
    else:
        total = Solicitud.objects.filter(usuario=usuario)
    context = {
        'usuario': usuario,
        'total_solicitudes': total.count(),
        'pendientes': total.filter(estado='PENDIENTE').count(),
        'en_proceso': total.filter(estado='EN_PROCESO').count(),
        'cerradas': total.filter(estado='CERRADA').count(),
        'recientes': total.order_by('-fecha_creacion')[:5],
    }
    return render(request, 'perfil.html', context)

# ─── MÓDULO ADMINISTRACIÓN DE USUARIOS ───

# Decorador para restringir acceso a administradores
def solo_admin(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.rol != 'ADMIN':
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('home:index')
        return view_func(request, *args, **kwargs)
    return wrapper

# Vista para listar usuarios con filtros y paginación
@login_required
@solo_admin
def lista_usuarios(request):
    usuarios_list = Usuario.objects.all().order_by('-date_joined')
    q = request.GET.get('q', '').strip()
    rol = request.GET.get('rol', '').strip()
    activo = request.GET.get('activo', '').strip()
    # Aplicar filtros de búsqueda
    if q:
        usuarios_list = usuarios_list.filter(
            Q(username__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(email__icontains=q) |
            Q(numero_identificacion__icontains=q)
        )
    if rol:
        usuarios_list = usuarios_list.filter(rol=rol)
    if activo:
        usuarios_list = usuarios_list.filter(is_active=activo == 'true')

    paginator = Paginator(usuarios_list, 10)
    page = request.GET.get('page', 1)
    try:
        usuarios = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        usuarios = paginator.page(1)
        
    context = {
        'usuarios': usuarios,
        'q': q,
        'rol': rol,
        'activo': activo,
        'rol_choices': Usuario.Rol.choices,
    }

    return render(request, 'lista_usuarios.html', context)

#vista para crear un nuevo usuario
@login_required
@solo_admin
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioAdminForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Usuario creado correctamente.')
                return redirect('usuarios:lista_usuarios')
            except Exception:
                messages.error(request, 'Ocurrió un error al crear el usuario.')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = UsuarioAdminForm()
    
    context = {
        'form': form,
        'titulo': 'Nuevo Usuario',
        'btn_texto': 'Crear usuario'
    }
    
    return render(request, 'form_usuario.html', context)

#vista para editar un usuario existente
@login_required
@solo_admin
def editar_usuario(request, id):
    
    
    
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'Usuario {usuario.first_name} {usuario.last_name} actualizado correctamente.')
                return redirect('usuarios:lista_usuarios')
            except Exception:
                messages.error(request, 'Ocurrió un error al actualizar el usuario.')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = EditarUsuarioForm(instance=usuario)
    return render(request, 'form_usuario.html', {
        'form': form,
        'titulo': f'Editar Usuario — {usuario.first_name} {usuario.last_name}',
        'btn_texto': 'Guardar cambios',
        'usuario': usuario
    })


@login_required
@solo_admin
def cambiar_contrasena(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not password1:
            messages.error(request, 'La contraseña no puede estar vacía.')
            return redirect('usuarios:lista_usuarios')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('usuarios:lista_usuarios')

        if len(password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return redirect('usuarios:lista_usuarios')

        usuario.set_password(password1)
        usuario.save()
        messages.success(request, f'Contraseña de {usuario.username} actualizada correctamente.')
    return redirect('usuarios:lista_usuarios')

@login_required
@solo_admin
def asignar_activo(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    
    # Validar que el usuario esté activo
    if not usuario.is_active:
        messages.error(request, f'No se puede asignar un activo a un usuario inactivo.')
        return redirect('usuarios:lista_usuarios')
    
    if request.method == 'POST':
        activo_id = request.POST.get('activo_id')
        
        if activo_id:
            activo = get_object_or_404(Activo, id=activo_id)

            # Si el activo tiene otro técnico asignado, desasignarlo primero
            if hasattr(activo, 'tecnico_asignado') and activo.tecnico_asignado and activo.tecnico_asignado != usuario:
                tecnico_anterior = activo.tecnico_asignado
                tecnico_anterior.activo_asignado = None
                tecnico_anterior.save()
                messages.info(request, f'Se desasignó a {tecnico_anterior.get_full_name()} del activo {activo.nombre}.')

            # Si el técnico ya tenía otro activo asignado, desasignarlo también
            if usuario.activo_asignado and usuario.activo_asignado != activo:
                messages.info(request, f'Se desasignó el activo anterior: {usuario.activo_asignado.nombre}.')

            usuario.activo_asignado = activo

        else:
            usuario.activo_asignado = None  

        usuario.save()
        if activo_id:
            messages.success(request, f'Activo {activo.nombre} actualizado correctamente para {usuario.get_full_name()}.')
        else:
            messages.success(request, f'Activo desasignado correctamente para {usuario.get_full_name()}.')
        return redirect('usuarios:lista_usuarios')

    # GET — retorna activos disponibles en JSON para el modal
    activos = Activo.objects.all().values('id', 'nombre', 'codigo')
    activos_data = []
    for activo in activos:
        try:
            tecnico = Activo.objects.get(id=activo['id']).tecnico_asignado
            ocupado = tecnico is not None and tecnico != usuario
            nombre_tecnico = tecnico.get_full_name() if ocupado else None
        except:
            ocupado = False
            nombre_tecnico = None
        
        activos_data.append({
            'id': activo['id'],
            'nombre': activo['nombre'],
            'codigo': activo['codigo'],
            'ocupado': ocupado,
            'tecnico': nombre_tecnico,
        })

    return JsonResponse({'activos': activos_data})


#vista para activar o desactivar un usuario
@login_required
@solo_admin
def toggle_usuario(request, id):
    """Activa o desactiva un usuario."""
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        if usuario == request.user:
            messages.error(request, 'No puedes desactivar tu propia cuenta.')
            return redirect('usuarios:lista_usuarios')
        
        usuario.is_active = not usuario.is_active
        
        if not usuario.is_active and usuario.activo_asignado:
            activo_nombre = usuario.activo_asignado.nombre
            usuario.activo_asignado = None
            messages.info(request, f'Se desvinculó el activo {activo_nombre} del usuario desactivado.')
        
        usuario.save()
        estado = 'activado' if usuario.is_active else 'desactivado'
        messages.success(request, f'Usuario {usuario.first_name} {usuario.last_name} {estado} correctamente.')
    return redirect('usuarios:lista_usuarios')

#vista para mostrar el detalle de un usuario y sus solicitudes recientes
@login_required
@solo_admin
def detalle_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    solicitudes = usuario.solicitudes_creadas.all().order_by('-fecha_creacion')[:10]
    return render(request, 'detalle_usuario.html', {
        'usuario': usuario,
        'solicitudes': solicitudes,
    })
    