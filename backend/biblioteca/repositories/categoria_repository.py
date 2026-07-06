from ..models import Categoria


def listar():
    return Categoria.objects.all()
