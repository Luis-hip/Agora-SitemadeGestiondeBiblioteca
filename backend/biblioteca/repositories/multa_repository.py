from ..models import Multa

RELACIONES_PRESTAMO = ('prestamo__libro__categoria',)
PREFETCH_AUTORES = ('prestamo__libro__autores',)


def contar_pendientes_por_usuario(usuario_id):
    return Multa.objects.filter(usuario_id=usuario_id, estado=Multa.Estado.PENDIENTE).count()


def buscar_pendiente_por_prestamo(prestamo_id):
    return Multa.objects.filter(prestamo_id=prestamo_id, estado=Multa.Estado.PENDIENTE).first()


def crear(*, prestamo, usuario_id, monto, dias_atraso):
    return Multa.objects.create(
        prestamo=prestamo,
        usuario_id=usuario_id,
        monto=monto,
        dias_atraso=dias_atraso,
        estado=Multa.Estado.PENDIENTE,
    )


def actualizar_monto(multa):
    multa.save(update_fields=['monto', 'dias_atraso', 'updated_at'])


def buscar_por_id_y_usuario_con_bloqueo(multa_id, usuario_id):
    return Multa.objects.select_for_update().filter(pk=multa_id, usuario_id=usuario_id).first()


def marcar_pagada(multa):
    multa.save(update_fields=['estado', 'fecha_pago', 'updated_at'])


def listar_por_usuario_y_estado(usuario_id, estado):
    return (
        Multa.objects.filter(usuario_id=usuario_id, estado=estado)
        .select_related(*RELACIONES_PRESTAMO)
        .prefetch_related(*PREFETCH_AUTORES)
        .order_by('-fecha_generacion')
    )
