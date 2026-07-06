from ..models import Libro


def listar(categoria_ids=None, disponible=None):
    queryset = Libro.objects.select_related('categoria').prefetch_related('autores')
    if categoria_ids:
        queryset = queryset.filter(categoria_id__in=categoria_ids)
    if disponible is not None:
        queryset = queryset.filter(disponible=disponible)
    return queryset


def buscar_por_id_con_bloqueo(libro_id):
    return Libro.objects.select_for_update().filter(pk=libro_id).first()


def marcar_no_disponible(libro):
    libro.disponible = False
    libro.save(update_fields=['disponible', 'updated_at'])


def descontar_stock(libro):
    libro.stock = max(libro.stock - 1, 0)
    libro.disponible = libro.stock > 0
    libro.save(update_fields=['stock', 'disponible', 'updated_at'])


def reponer_stock(libro):
    libro.stock += 1
    libro.disponible = True
    libro.save(update_fields=['stock', 'disponible', 'updated_at'])
