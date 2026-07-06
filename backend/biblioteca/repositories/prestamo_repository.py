from ..models import Prestamo


def contar_activos_por_usuario(usuario_id):
    return Prestamo.objects.filter(usuario_id=usuario_id, estado=Prestamo.Estado.ACTIVO).count()


def buscar_por_id_con_bloqueo(prestamo_id):
    return Prestamo.objects.select_for_update().filter(pk=prestamo_id).first()


def crear(*, usuario, libro, bibliotecario_id, fecha_dev_esperada):
    return Prestamo.objects.create(
        usuario=usuario,
        libro=libro,
        bibliotecario_id=bibliotecario_id,
        fecha_dev_esperada=fecha_dev_esperada,
        estado=Prestamo.Estado.ACTIVO,
    )


def _con_relaciones(queryset):
    return queryset.select_related('libro__categoria', 'bibliotecario').prefetch_related('libro__autores')


def listar_por_usuario(usuario_id):
    return _con_relaciones(Prestamo.objects.filter(usuario_id=usuario_id)).order_by('-fecha_inicio')


def listar_activos_por_usuario(usuario_id):
    return _con_relaciones(
        Prestamo.objects.filter(usuario_id=usuario_id, estado=Prestamo.Estado.ACTIVO)
    ).order_by('-fecha_inicio')
