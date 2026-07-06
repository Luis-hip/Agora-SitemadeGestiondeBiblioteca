from ..repositories import autor_repository, categoria_repository, libro_repository

VALORES_VERDADEROS = {'true', '1', 'si', 'yes'}
VALORES_FALSOS = {'false', '0', 'no'}


def _parsear_disponible(valor):
    if valor is None:
        return None
    valor_normalizado = str(valor).strip().lower()
    if valor_normalizado in VALORES_VERDADEROS:
        return True
    if valor_normalizado in VALORES_FALSOS:
        return False
    return None


def _parsear_categoria_ids(valor):
    if not valor:
        return None
    ids = []
    for parte in str(valor).split(','):
        parte = parte.strip()
        if parte.isdigit():
            ids.append(int(parte))
    return ids or None


def listar_libros(categoria_id=None, disponible=None):
    return libro_repository.listar(
        categoria_ids=_parsear_categoria_ids(categoria_id), disponible=_parsear_disponible(disponible),
    )


def listar_categorias():
    return categoria_repository.listar()


def listar_autores():
    return autor_repository.listar()
