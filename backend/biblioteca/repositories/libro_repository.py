from ..models import Libro


def listar(categoria_id=None, disponible=None):
    queryset = Libro.objects.select_related('categoria').prefetch_related('autores')
    if categoria_id:
        queryset = queryset.filter(categoria_id=categoria_id)
    if disponible is not None:
        queryset = queryset.filter(disponible=disponible)
    return queryset


def buscar_por_id_con_bloqueo(libro_id):
    return Libro.objects.select_for_update().filter(pk=libro_id).first()


def marcar_no_disponible(libro):
    libro.disponible = False
    libro.save(update_fields=['disponible', 'updated_at'])
