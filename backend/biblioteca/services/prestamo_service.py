from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from ..exceptions import ReglaDeNegocioError, RecursoNoEncontradoError
from ..models import ConfiguracionBiblioteca, Usuario
from ..repositories import libro_repository, multa_repository, prestamo_repository, usuario_repository

LIMITE_PRESTAMOS_ACTIVOS = 3


class PrestamoService:
    @transaction.atomic
    def registrar_prestamo(self, usuario_id, libro_id, bibliotecario_id=None):
        # 1) Validacion de existencia y estado (RF-04)
        usuario = usuario_repository.buscar_por_id_con_bloqueo(usuario_id)
        if usuario is None:
            raise RecursoNoEncontradoError('Usuario no registrado')
        if usuario.estado != Usuario.Estado.ACTIVO:
            raise ReglaDeNegocioError('USR_INACTIVO', 'El usuario no se encuentra activo')

        # 2) Bloqueo por multas pendientes (RN-03)
        if multa_repository.contar_pendientes_por_usuario(usuario_id) > 0:
            raise ReglaDeNegocioError('MULTA_ACTIVA', 'El usuario tiene multas pendientes de pago')

        # 3) Limite de prestamos simultaneos (RN-01)
        if prestamo_repository.contar_activos_por_usuario(usuario_id) >= LIMITE_PRESTAMOS_ACTIVOS:
            raise ReglaDeNegocioError('LIMITE_PRESTAMOS', 'El usuario alcanzo el limite de prestamos simultaneos')

        # 4) Disponibilidad exclusiva del ejemplar (RN-04)
        libro = libro_repository.buscar_por_id_con_bloqueo(libro_id)
        if libro is None:
            raise RecursoNoEncontradoError('Libro no encontrado en catalogo')
        if not libro.disponible:
            raise ReglaDeNegocioError('LIBRO_NO_DISPONIBLE', 'El ejemplar no esta disponible para prestamo')

        # 5) Calculo de fecha limite y persistencia atomica (RN-02, RN-04)
        dias_prestamo = ConfiguracionBiblioteca.cargar().dias_maximos_prestamo
        fecha_dev_esperada = timezone.localdate() + timedelta(days=dias_prestamo)

        nuevo_prestamo = prestamo_repository.crear(
            usuario=usuario,
            libro=libro,
            bibliotecario_id=bibliotecario_id,
            fecha_dev_esperada=fecha_dev_esperada,
        )
        libro_repository.marcar_no_disponible(libro)

        return nuevo_prestamo
