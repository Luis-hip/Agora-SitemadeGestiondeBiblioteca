from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from .api_response import respuesta_estandar
from .exceptions import RecursoNoEncontradoError, ReglaDeNegocioError
from .models import Bibliotecario
from .serializers import (
    CategoriaSerializer,
    LibroSerializer,
    LoginSerializer,
    PrestamoRequestSerializer,
    PrestamoSerializer,
    RegistroUsuarioSerializer,
)
from .services import auth_service, catalogo_service
from .services.prestamo_service import PrestamoService


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


class CatalogoLibroViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LibroSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_queryset(self):
        return catalogo_service.listar_libros(
            categoria_id=self.request.query_params.get('categoria'),
            disponible=self.request.query_params.get('disponible'),
        )


class CatalogoCategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategoriaSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_queryset(self):
        return catalogo_service.listar_categorias()


class PrestamoController(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PrestamoRequestSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            return respuesta_estandar(False, 400, mensaje='Datos invalidos.', detalle=exc.detail)

        actor = request.user
        if isinstance(actor, Bibliotecario):
            usuario_id = serializer.validated_data.get('usuario_id')
            if not usuario_id:
                return respuesta_estandar(
                    False, 400,
                    mensaje='Debe indicar el usuario para el cual se registra el prestamo.',
                )
            bibliotecario_id = actor.id
        else:
            usuario_id = actor.id
            bibliotecario_id = None

        try:
            prestamo = PrestamoService().registrar_prestamo(
                usuario_id, serializer.validated_data['libro_id'], bibliotecario_id,
            )
        except RecursoNoEncontradoError as exc:
            return respuesta_estandar(False, exc.status_http, mensaje=exc.mensaje, detalle=exc.codigo)
        except ReglaDeNegocioError as exc:
            return respuesta_estandar(False, exc.status_http, mensaje=exc.mensaje, detalle=exc.codigo)

        return respuesta_estandar(
            True, 201,
            datos=PrestamoSerializer(prestamo).data,
            mensaje='Prestamo registrado',
        )
