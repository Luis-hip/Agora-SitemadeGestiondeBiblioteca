from ..models import Multa
from ..repositories import multa_repository, prestamo_repository


def obtener_perfil(usuario):
    return {
        'prestamos_activos': prestamo_repository.listar_activos_por_usuario(usuario.id),
        'historial_prestamos': prestamo_repository.listar_por_usuario(usuario.id),
        'multas_pendientes': multa_repository.listar_por_usuario_y_estado(usuario.id, Multa.Estado.PENDIENTE),
        'multas_pagadas': multa_repository.listar_por_usuario_y_estado(usuario.id, Multa.Estado.PAGADA),
    }
