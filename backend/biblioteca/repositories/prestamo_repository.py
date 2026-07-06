from ..models import Prestamo


def contar_activos_por_usuario(usuario_id):
    return Prestamo.objects.filter(usuario_id=usuario_id, estado=Prestamo.Estado.ACTIVO).count()


def crear(*, usuario, libro, bibliotecario_id, fecha_dev_esperada):
    return Prestamo.objects.create(
        usuario=usuario,
        libro=libro,
        bibliotecario_id=bibliotecario_id,
        fecha_dev_esperada=fecha_dev_esperada,
        estado=Prestamo.Estado.ACTIVO,
    )
