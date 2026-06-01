import pytest
from django.core.exceptions import ValidationError
from solicitudes.models import Solicitud, Seguimiento
from activos.models import Activo, Sistema
from django.contrib.auth import get_user_model

Usuario = get_user_model()

@pytest.fixture
def usuario(db):
    return Usuario.objects.create_user(
        username='tecnico_prueba1',
        password='Prueba12345',
        first_name='Técnico',
        last_name='Prueba',
    )

@pytest.fixture
def activo(db):
    return Activo.objects.create(nombre='Compresor C-01', marca='Atlas')

@pytest.fixture
def sistema(db, activo):
    return Sistema.objects.create(nombre='Sistema Eléctrico', activo=activo)

@pytest.fixture
def solicitud_pendiente(db, usuario, activo, sistema):
    return Solicitud.todos.create(
        usuario=usuario,
        activo=activo,
        sistema_activo=sistema,
        titulo='Falla en compresor',
        descripcion='El compresor no enciende',
        repuestos_necesarios='Fusible 10A',
        criticidad=3,
        estado='PENDIENTE'
    )


# ─── PRUEBA 1 ───
# Valida que no se puede pasar directamente de PENDIENTE a CERRADA
@pytest.mark.django_db
def test_no_se_puede_cerrar_desde_pendiente(solicitud_pendiente):
    with pytest.raises(ValueError):
        solicitud_pendiente.cerrar(trabajo_realizado='Trabajo de prueba')


# ─── PRUEBA 2 ───
# Valida que el flujo correcto PENDIENTE → EN_PROCESO → CERRADA funciona
@pytest.mark.django_db
def test_flujo_completo_solicitud(solicitud_pendiente):
    solicitud_pendiente.iniciar_proceso()
    assert solicitud_pendiente.estado == 'EN_PROCESO'

    solicitud_pendiente.cerrar(
        trabajo_realizado='Se reemplazó el fusible',
        observaciones_cierre='Equipo operativo'
    )
    assert solicitud_pendiente.estado == 'CERRADA'
    assert solicitud_pendiente.fecha_cierre is not None


# ─── PRUEBA 3 ───
# Valida que no se puede eliminar una solicitud que no está PENDIENTE
@pytest.mark.django_db
def test_no_se_puede_eliminar_solicitud_en_proceso(solicitud_pendiente):
    solicitud_pendiente.iniciar_proceso()
    with pytest.raises(ValidationError):
        solicitud_pendiente.delete()


# ─── PRUEBA 4 ───
# Valida que los seguimientos no se pueden eliminar
@pytest.mark.django_db
def test_seguimiento_no_se_puede_eliminar(solicitud_pendiente, usuario):
    seguimiento = Seguimiento.objects.create(
        solicitud=solicitud_pendiente,
        usuario=usuario,
        comentario='Creación de orden|La orden fue creada en estado Pendiente.'
    )
    with pytest.raises(ValidationError):
        seguimiento.delete()