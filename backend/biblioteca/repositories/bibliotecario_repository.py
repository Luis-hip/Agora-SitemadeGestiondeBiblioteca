from ..models import Bibliotecario


def buscar_por_usuario_sistema(usuario_sistema):
    return Bibliotecario.objects.filter(usuario_sistema=usuario_sistema).first()
