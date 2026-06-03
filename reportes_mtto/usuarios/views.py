from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import  UsuarioAdminForm, EditarUsuarioForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm

Usuario = get_user_model()



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

@login_required
def perfil_usuario(request):
    from solicitudes.models import Solicitud
    usuario = request.user
    total = Solicitud.todos.filter(usuario=usuario)
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
    