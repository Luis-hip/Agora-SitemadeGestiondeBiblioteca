from datetime import timedelta

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .api_response import respuesta_estandar
from .exceptions import RecursoNoEncontradoError
from .models import ConfiguracionBiblioteca, Devolucion, Multa, Prestamo, Usuario
from .permissions import EsBibliotecario
from .serializers import (
    AdminMultaSerializer,
    AdminPrestamoSerializer,
    ConfiguracionBibliotecaSerializer,
    DevolucionSerializer,
    MultaSerializer,
    PrestamoSerializer,
    UsuarioSerializer,
)
from .services import dashboard_service, perfil_service, usuario_service


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, EsBibliotecario]

    def get(self, request):
        kpis = dashboard_service.obtener_kpis()
        actividad_reciente = dashboard_service.obtener_actividad_reciente()

        return respuesta_estandar(
            True, 200,
            datos={
                'kpis': kpis,
                'actividad_reciente': AdminPrestamoSerializer(actividad_reciente, many=True).data,
            },
            mensaje='Dashboard obtenido correctamente.',
        )


class AdminPrestamoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AdminPrestamoSerializer
    permission_classes = [IsAuthenticated, EsBibliotecario]

    def get_queryset(self):
        queryset = (
            Prestamo.objects.select_related('usuario', 'libro__categoria', 'bibliotecario')
            .prefetch_related('libro__autores')
            .order_by('-fecha_inicio')
        )

        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)

        if self.request.query_params.get('vence_pronto') == 'true':
            hoy = timezone.localdate()
            limite = hoy + timedelta(days=2)
            queryset = queryset.filter(
                estado=Prestamo.Estado.ACTIVO, fecha_dev_esperada__gte=hoy, fecha_dev_esperada__lte=limite,
            )

        return queryset


class AdminDevolucionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DevolucionSerializer
    permission_classes = [IsAuthenticated, EsBibliotecario]

    def get_queryset(self):
        fecha = self.request.query_params.get('fecha') or timezone.localdate().isoformat()
        return (
            Devolucion.objects.filter(fecha_devolucion=fecha)
            .select_related('prestamo__usuario', 'prestamo__libro__categoria', 'prestamo__bibliotecario')
            .prefetch_related('prestamo__libro__autores')
            .order_by('-fecha_devolucion')
        )


class AdminMultaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AdminMultaSerializer
    permission_classes = [IsAuthenticated, EsBibliotecario]

    def get_queryset(self):
        queryset = (
            Multa.objects.select_related('prestamo__usuario', 'prestamo__libro__categoria', 'prestamo__bibliotecario')
            .prefetch_related('prestamo__libro__autores')
            .order_by('-fecha_generacion')
        )
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset


class AdminUsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, EsBibliotecario]
    queryset = Usuario.objects.all().order_by('nombre')

    def retrieve(self, request, *args, **kwargs):
        usuario = self.get_object()
        perfil = perfil_service.obtener_perfil(usuario)

        return respuesta_estandar(
            True, 200,
            datos={
                'usuario': UsuarioSerializer(usuario).data,
                'prestamos_activos': PrestamoSerializer(perfil['prestamos_activos'], many=True).data,
                'historial_prestamos': PrestamoSerializer(perfil['historial_prestamos'], many=True).data,
                'multas_pendientes': MultaSerializer(perfil['multas_pendientes'], many=True).data,
                'multas_pagadas': MultaSerializer(perfil['multas_pagadas'], many=True).data,
            },
            mensaje='Detalle de usuario obtenido correctamente.',
        )

    @action(detail=True, methods=['post'])
    def suspender(self, request, pk=None):
        try:
            usuario = usuario_service.suspender_manualmente(pk)
        except RecursoNoEncontradoError as exc:
            return respuesta_estandar(False, exc.status_http, mensaje=exc.mensaje, detalle=exc.codigo)

        return respuesta_estandar(
            True, 200, datos=UsuarioSerializer(usuario).data, mensaje='Usuario suspendido correctamente.',
        )


class AdminConfiguracionView(APIView):
    permission_classes = [IsAuthenticated, EsBibliotecario]

    def get(self, request):
        configuracion = ConfiguracionBiblioteca.cargar()
        return respuesta_estandar(
            True, 200,
            datos=ConfiguracionBibliotecaSerializer(configuracion).data,
            mensaje='Configuracion obtenida correctamente.',
        )

    def patch(self, request):
        configuracion = ConfiguracionBiblioteca.cargar()
        serializer = ConfiguracionBibliotecaSerializer(configuracion, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            return respuesta_estandar(False, 400, mensaje='Datos invalidos.', detalle=exc.detail)
        serializer.save()

        return respuesta_estandar(
            True, 200,
            datos=serializer.data,
            mensaje='Configuracion actualizada correctamente.',
        )
