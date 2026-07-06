from django.db import transaction

from ..exceptions import RecursoNoEncontradoError
from ..models import Usuario
from ..repositories import usuario_repository


@transaction.atomic
def suspender_manualmente(usuario_id):
    usuario = usuario_repository.buscar_por_id_con_bloqueo(usuario_id)
    if usuario is None:
        raise RecursoNoEncontradoError('Usuario no encontrado')

    usuario.estado = Usuario.Estado.SUSPENDIDO
    usuario_repository.actualizar_estado(usuario)
    return usuario
