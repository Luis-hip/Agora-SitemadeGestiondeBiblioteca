from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .api_response import respuesta_estandar
from .exceptions import ReglaDeNegocioError
from .serializers import LoginSerializer, RegistroUsuarioSerializer
from .services import auth_service


class RegistroUsuarioView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistroUsuarioSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            return respuesta_estandar(False, 400, mensaje='Datos invalidos.', detalle=exc.detail)

        usuario = auth_service.registrar_usuario(serializer.validated_data)
        tokens = auth_service.generar_tokens(usuario, 'USUARIO', usuario.tipo_usuario)

        return respuesta_estandar(
            True, 201,
            datos={
                'access': tokens['access'],
                'refresh': tokens['refresh'],
                'actor': {
                    'id': usuario.id,
                    'nombre': usuario.nombre,
                    'email': usuario.email,
                    'rol': usuario.tipo_usuario,
                },
            },
            mensaje='Usuario registrado exitosamente.',
        )


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            return respuesta_estandar(False, 400, mensaje='Datos invalidos.', detalle=exc.detail)

        try:
            actor, tipo_actor, rol = auth_service.autenticar(
                serializer.validated_data['identificador'],
                serializer.validated_data['password'],
            )
        except ReglaDeNegocioError as exc:
            return respuesta_estandar(False, exc.status_http, mensaje=exc.mensaje, detalle=exc.codigo)

        tokens = auth_service.generar_tokens(actor, tipo_actor, rol)

        return respuesta_estandar(
            True, 200,
            datos={
                'access': tokens['access'],
                'refresh': tokens['refresh'],
                'actor': {
                    'id': actor.id,
                    'nombre': actor.nombre,
                    'rol': rol,
                    'tipo_actor': tipo_actor,
                },
            },
            mensaje='Inicio de sesion exitoso.',
        )
