from django.db.models import ProtectedError
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from .api_response import respuesta_estandar
from .exceptions import RecursoNoEncontradoError, ReglaDeNegocioError
from .models import Bibliotecario
from .permissions import EsBibliotecario, EsUsuario
from .serializers import (
    AnularMultaRequestSerializer,
    AutorSerializer,
    CalculoMultaRequestSerializer,
    CategoriaSerializer,
    LibroEscrituraSerializer,
    LibroSerializer,
    LoginSerializer,
    MultaSerializer,
    PrestamoRequestSerializer,
    PrestamoSerializer,
    RegistroUsuarioSerializer,
    UsuarioSerializer,
)
from .services import auth_service, catalogo_service, perfil_service
from .services.multa_service import MultaService
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


class CatalogoLibroViewSet(viewsets.ModelViewSet):
    serializer_class = LibroSerializer

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return LibroEscrituraSerializer
        return LibroSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), EsBibliotecario()]

    def get_queryset(self):
        return catalogo_service.listar_libros(
            categoria_id=self.request.query_params.get('categoria'),
            disponible=self.request.query_params.get('disponible'),
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
        except ProtectedError:
            return respuesta_estandar(
                False, 422,
                mensaje='No se puede eliminar: el libro tiene prestamos asociados.',
                detalle='LIBRO_CON_PRESTAMOS',
            )
        return respuesta_estandar(True, 200, mensaje='Libro eliminado correctamente.')


class CatalogoCategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), EsBibliotecario()]

    def get_queryset(self):
        return catalogo_service.listar_categorias()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
        except ProtectedError:
            return respuesta_estandar(
                False, 422,
                mensaje='No se puede eliminar: existen libros asociados a esta categoria.',
                detalle='CATEGORIA_CON_LIBROS',
            )
        return respuesta_estandar(True, 200, mensaje='Categoria eliminada correctamente.')


class CatalogoAutorViewSet(viewsets.ModelViewSet):
    serializer_class = AutorSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), EsBibliotecario()]

    def get_queryset(self):
        return catalogo_service.listar_autores()


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


class PerfilView(APIView):
    permission_classes = [IsAuthenticated, EsUsuario]

    def get(self, request):
        perfil = perfil_service.obtener_perfil(request.user)

        return respuesta_estandar(
            True, 200,
            datos={
                'usuario': UsuarioSerializer(request.user).data,
                'prestamos_activos': PrestamoSerializer(perfil['prestamos_activos'], many=True).data,
                'historial_prestamos': PrestamoSerializer(perfil['historial_prestamos'], many=True).data,
                'multas_pendientes': MultaSerializer(perfil['multas_pendientes'], many=True).data,
                'multas_pagadas': MultaSerializer(perfil['multas_pagadas'], many=True).data,
            },
            mensaje='Perfil obtenido correctamente.',
        )


class MultaController(APIView):
    permission_classes = [IsAuthenticated, EsBibliotecario]

    def post(self, request):
        serializer = CalculoMultaRequestSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            return respuesta_estandar(False, 400, mensaje='Datos invalidos.', detalle=exc.detail)

        try:
            multa = MultaService().calcular_y_registrar(
                serializer.validated_data['prestamo_id'],
                serializer.validated_data['fecha_devolucion_real'],
            )
        except RecursoNoEncontradoError as exc:
            return respuesta_estandar(False, exc.status_http, mensaje=exc.mensaje, detalle=exc.codigo)
        except ReglaDeNegocioError as exc:
            return respuesta_estandar(False, exc.status_http, mensaje=exc.mensaje, detalle=exc.codigo)

        if multa is None:
            return respuesta_estandar(
                True, 200, datos=None, mensaje='Devolucion registrada dentro del plazo; no se genera multa.',
            )
        return respuesta_estandar(True, 201, datos=MultaSerializer(multa).data, mensaje='Multa procesada')


class MultaPagoController(APIView):
    permission_classes = [IsAuthenticated, EsUsuario]

    def post(self, request, multa_id):
        try:
            multa = MultaService().pagar(multa_id, request.user.id)
        except RecursoNoEncontradoError as exc:
            return respuesta_estandar(False, exc.status_http, mensaje=exc.mensaje, detalle=exc.codigo)
        except ReglaDeNegocioError as exc:
            return respuesta_estandar(False, exc.status_http, mensaje=exc.mensaje, detalle=exc.codigo)

        return respuesta_estandar(True, 200, datos=MultaSerializer(multa).data, mensaje='Multa pagada exitosamente')


class MultaAnularController(APIView):
    permission_classes = [IsAuthenticated, EsBibliotecario]

    def post(self, request, multa_id):
        serializer = AnularMultaRequestSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            return respuesta_estandar(False, 400, mensaje='Datos invalidos.', detalle=exc.detail)

        try:
            multa = MultaService().anular_multa(
                multa_id, serializer.validated_data['justificacion'], request.user,
            )
        except RecursoNoEncontradoError as exc:
            return respuesta_estandar(False, exc.status_http, mensaje=exc.mensaje, detalle=exc.codigo)
        except ReglaDeNegocioError as exc:
            return respuesta_estandar(False, exc.status_http, mensaje=exc.mensaje, detalle=exc.codigo)

        return respuesta_estandar(True, 200, datos=MultaSerializer(multa).data, mensaje='Multa anulada exitosamente')
