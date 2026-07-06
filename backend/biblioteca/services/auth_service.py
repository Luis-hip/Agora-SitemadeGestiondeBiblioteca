from rest_framework_simplejwt.tokens import RefreshToken

from ..authentication import TIPO_ACTOR_BIBLIOTECARIO, TIPO_ACTOR_USUARIO
from ..exceptions import CredencialesInvalidasError, CuentaInactivaError
from ..repositories import bibliotecario_repository, usuario_repository

ROL_BIBLIOTECARIO = 'BIBLIOTECARIO'


def registrar_usuario(datos):
    return usuario_repository.crear(
        email=datos['email'],
        matricula=datos['matricula'],
        nombre=datos['nombre'],
        telefono=datos['telefono'],
        tipo_usuario=datos['tipo_usuario'],
        password=datos['password'],
    )


def autenticar(identificador, password):
    usuario = usuario_repository.buscar_por_email(identificador)
    if usuario is not None and usuario.check_password(password):
        if not usuario.is_active:
            raise CuentaInactivaError()
        return usuario, TIPO_ACTOR_USUARIO, usuario.tipo_usuario

    bibliotecario = bibliotecario_repository.buscar_por_usuario_sistema(identificador)
    if bibliotecario is not None and bibliotecario.check_password(password):
        if not bibliotecario.is_active:
            raise CuentaInactivaError()
        return bibliotecario, TIPO_ACTOR_BIBLIOTECARIO, ROL_BIBLIOTECARIO

    raise CredencialesInvalidasError()


def generar_tokens(actor, tipo_actor, rol):
    refresh = RefreshToken.for_user(actor)
    refresh['tipo_actor'] = tipo_actor
    refresh['rol'] = rol
    refresh['nombre'] = actor.nombre
    access = refresh.access_token

    return {
        'access': str(access),
        'refresh': str(refresh),
    }
