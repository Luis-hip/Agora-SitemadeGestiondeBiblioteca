from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CatalogoCategoriaViewSet,
    CatalogoLibroViewSet,
    LoginView,
    MultaController,
    MultaPagoController,
    PerfilView,
    PrestamoController,
    RegistroUsuarioView,
)

router = DefaultRouter()
router.register('catalogo/libros', CatalogoLibroViewSet, basename='catalogo-libros')
router.register('catalogo/categorias', CatalogoCategoriaViewSet, basename='catalogo-categorias')

urlpatterns = [
    path('auth/registro/', RegistroUsuarioView.as_view(), name='auth-registro'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('prestamos/', PrestamoController.as_view(), name='prestamos-crear'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('multas/calcular/', MultaController.as_view(), name='multas-calcular'),
    path('multas/<int:multa_id>/pagar/', MultaPagoController.as_view(), name='multas-pagar'),
] + router.urls
