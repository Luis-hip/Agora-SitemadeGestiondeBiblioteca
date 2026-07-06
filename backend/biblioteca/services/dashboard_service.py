from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone

from ..models import Devolucion, Multa, Prestamo

HORAS_VENCIMIENTO_PROXIMO = 48
LIMITE_ACTIVIDAD_RECIENTE = 10


def obtener_kpis():
    hoy = timezone.localdate()
    # fecha_dev_esperada es un DateField (sin componente horario), por lo que las 48 horas
    # se expresan como dias completos para la comparacion.
    limite_vencimiento = hoy + timedelta(days=HORAS_VENCIMIENTO_PROXIMO // 24)

    prestamos_activos = Prestamo.objects.filter(estado=Prestamo.Estado.ACTIVO).count()
    devoluciones_hoy = Devolucion.objects.filter(fecha_devolucion=hoy).count()
    multas_pendientes_total = (
        Multa.objects.filter(estado=Multa.Estado.PENDIENTE).aggregate(total=Sum('monto'))['total'] or 0
    )
    vencimientos_proximos = Prestamo.objects.filter(
        estado=Prestamo.Estado.ACTIVO,
        fecha_dev_esperada__gte=hoy,
        fecha_dev_esperada__lte=limite_vencimiento,
    ).count()

    return {
        'prestamos_activos': prestamos_activos,
        'devoluciones_hoy': devoluciones_hoy,
        'multas_pendientes_total': str(multas_pendientes_total),
        'vencimientos_proximos': vencimientos_proximos,
    }


def obtener_actividad_reciente(limite=LIMITE_ACTIVIDAD_RECIENTE):
    return (
        Prestamo.objects.select_related('usuario', 'libro__categoria', 'bibliotecario')
        .prefetch_related('libro__autores')
        .order_by('-created_at')[:limite]
    )
