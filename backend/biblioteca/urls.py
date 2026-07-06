from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CatalogoCategoriaViewSet,
    CatalogoLibroViewSet,
    LoginView,
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
] + router.urls
