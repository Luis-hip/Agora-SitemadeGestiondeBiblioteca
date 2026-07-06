from django.conf import settings
from django.db import transaction
from django.utils import timezone

from ..exceptions import ReglaDeNegocioError, RecursoNoEncontradoError
from ..models import Bibliotecario, Multa, Usuario
from ..repositories import multa_repository, prestamo_repository, usuario_repository


class MultaService:
    @transaction.atomic
    def calcular_y_registrar(self, prestamo_id, fecha_devolucion_real):
        prestamo = prestamo_repository.buscar_por_id_con_bloqueo(prestamo_id)
        if prestamo is None:
            raise RecursoNoEncontradoError('Prestamo no encontrado')

        # 1) Dias de atraso (RN-02: coherencia cronologica)
        dias_atraso = (fecha_devolucion_real - prestamo.fecha_dev_esperada).days

        if dias_atraso <= 0:
            raise ReglaDeNegocioError('SIN_ATRASO', 'La devolucion se realizo dentro del plazo, no se genera multa')

        # 2) Monto no editable, derivado de formula (RN-05)
        monto = round(settings.TARIFA_MULTA_DIA * dias_atraso, 2)

        # 3) Evitar duplicidad: actualizar si ya existe multa activa
        multa_existente = multa_repository.buscar_pendiente_por_prestamo(prestamo_id)
        if multa_existente is not None:
            multa_existente.monto = monto
            multa_existente.dias_atraso = dias_atraso
            multa_repository.actualizar_monto(multa_existente)
            multa_final = multa_existente
        else:
            multa_final = multa_repository.crear(
                prestamo=prestamo, usuario_id=prestamo.usuario_id, monto=monto, dias_atraso=dias_atraso,
            )

        # 4) Suspension automatica del usuario (RN-03)
        usuario = usuario_repository.buscar_por_id_con_bloqueo(prestamo.usuario_id)
        usuario.estado = Usuario.Estado.SUSPENDIDO
        usuario_repository.actualizar_estado(usuario)

        return multa_final

    @transaction.atomic
    def pagar(self, multa_id, usuario_id):
        multa = multa_repository.buscar_por_id_y_usuario_con_bloqueo(multa_id, usuario_id)
        if multa is None:
            raise RecursoNoEncontradoError('Multa no encontrada')
        if multa.estado != Multa.Estado.PENDIENTE:
            raise ReglaDeNegocioError('MULTA_NO_PENDIENTE', 'La multa no se encuentra pendiente de pago')

        multa.estado = Multa.Estado.PAGADA
        multa.fecha_pago = timezone.localdate()
        multa_repository.marcar_pagada(multa)

        # RN-03: el bloqueo se levanta automaticamente solo si no quedan otras multas pendientes
        if multa_repository.contar_pendientes_por_usuario(usuario_id) == 0:
            usuario = usuario_repository.buscar_por_id_con_bloqueo(usuario_id)
            usuario.estado = Usuario.Estado.ACTIVO
            usuario_repository.actualizar_estado(usuario)

        return multa

    @transaction.atomic
    def anular_multa(self, multa_id, justificacion, usuario_ejecutor):
        if not isinstance(usuario_ejecutor, Bibliotecario):
            raise ReglaDeNegocioError('ROL_NO_AUTORIZADO', 'Solo un bibliotecario puede anular una multa.')

        multa = multa_repository.buscar_por_id_con_bloqueo(multa_id)
        if multa is None:
            raise RecursoNoEncontradoError('Multa no encontrada')
        if multa.estado != Multa.Estado.PENDIENTE:
            raise ReglaDeNegocioError('MULTA_NO_PENDIENTE', 'La multa no se encuentra pendiente de pago')

        multa.estado = Multa.Estado.ANULADA
        multa.justificacion_anulacion = justificacion
        multa_repository.marcar_anulada(multa)

        # RN-03: el bloqueo se levanta automaticamente solo si no quedan otras multas pendientes
        if multa_repository.contar_pendientes_por_usuario(multa.usuario_id) == 0:
            usuario = usuario_repository.buscar_por_id_con_bloqueo(multa.usuario_id)
            usuario.estado = Usuario.Estado.ACTIVO
            usuario_repository.actualizar_estado(usuario)

        return multa
