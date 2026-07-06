from ..models import Multa


def contar_pendientes_por_usuario(usuario_id):
    return Multa.objects.filter(usuario_id=usuario_id, estado=Multa.Estado.PENDIENTE).count()
