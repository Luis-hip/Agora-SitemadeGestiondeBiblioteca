from ..models import Autor


def listar():
    return Autor.objects.all().order_by('nombre')
