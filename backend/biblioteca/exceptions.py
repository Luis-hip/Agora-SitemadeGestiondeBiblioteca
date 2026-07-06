class ReglaDeNegocioError(Exception):
    status_http = 422

    def __init__(self, codigo, mensaje):
        self.codigo = codigo
        self.mensaje = mensaje
        super().__init__(mensaje)


class CredencialesInvalidasError(ReglaDeNegocioError):
    status_http = 401

    def __init__(self, mensaje='Correo/usuario o contrasena incorrectos.'):
        super().__init__('CREDENCIALES_INVALIDAS', mensaje)


class CuentaInactivaError(ReglaDeNegocioError):
    status_http = 403

    def __init__(self, mensaje='La cuenta se encuentra inactiva.'):
        super().__init__('CUENTA_INACTIVA', mensaje)


class RecursoNoEncontradoError(Exception):
    status_http = 404
    codigo = 'RECURSO_NO_ENCONTRADO'

    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(mensaje)
