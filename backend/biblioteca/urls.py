from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CatalogoAutorViewSet,
    CatalogoCategoriaViewSet,
    CatalogoLibroViewSet,
    LoginView,
    MultaAnularController,
    MultaController,
    MultaPagoController,
    PerfilView,
    PrestamoController,
    RegistroUsuarioView,
)
from .views_admin import (
    AdminDashboardView,
    AdminDevolucionViewSet,
    AdminMultaViewSet,
    AdminPrestamoViewSet,
    AdminUsuarioViewSet,
)

router = DefaultRouter()
router.register('catalogo/libros', CatalogoLibroViewSet, basename='catalogo-libros')
router.register('catalogo/categorias', CatalogoCategoriaViewSet, basename='catalogo-categorias')
router.register('catalogo/autores', CatalogoAutorViewSet, basename='catalogo-autores')
router.register('admin/usuarios', AdminUsuarioViewSet, basename='admin-usuarios')
router.register('admin/prestamos', AdminPrestamoViewSet, basename='admin-prestamos')
router.register('admin/devoluciones', AdminDevolucionViewSet, basename='admin-devoluciones')
router.register('admin/multas', AdminMultaViewSet, basename='admin-multas')

urlpatterns = [
    path('auth/registro/', RegistroUsuarioView.as_view(), name='auth-registro'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('prestamos/', PrestamoController.as_view(), name='prestamos-crear'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('multas/calcular/', MultaController.as_view(), name='multas-calcular'),
    path('multas/<int:multa_id>/pagar/', MultaPagoController.as_view(), name='multas-pagar'),
    path('multas/<int:multa_id>/anular/', MultaAnularController.as_view(), name='multas-anular'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
] + router.urls
