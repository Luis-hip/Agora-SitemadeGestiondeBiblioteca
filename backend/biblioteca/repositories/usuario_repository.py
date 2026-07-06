from ..models import Usuario


def crear(*, email, matricula, nombre, telefono, tipo_usuario, password):
    return Usuario.objects.create_user(
        email=email,
        matricula=matricula,
        nombre=nombre,
        telefono=telefono,
        tipo_usuario=tipo_usuario,
        password=password,
    )


def buscar_por_email(email):
    return Usuario.objects.filter(email__iexact=email).first()


def existe_email(email):
    return Usuario.objects.filter(email__iexact=email).exists()


def existe_matricula(matricula):
    return Usuario.objects.filter(matricula=matricula).exists()


def buscar_por_id_con_bloqueo(usuario_id):
    return Usuario.objects.select_for_update().filter(pk=usuario_id).first()


def actualizar_estado(usuario):
    usuario.save(update_fields=['estado', 'updated_at'])


def listar_todos():
    return Usuario.objects.all().order_by('nombre')
