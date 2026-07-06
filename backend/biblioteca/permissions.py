from rest_framework.permissions import BasePermission

from .models import Bibliotecario, Usuario


class EsBibliotecario(BasePermission):
    message = 'Esta accion solo esta disponible para bibliotecarios.'

    def has_permission(self, request, view):
        return isinstance(request.user, Bibliotecario)


class EsUsuario(BasePermission):
    message = 'Esta accion solo esta disponible para usuarios (estudiantes/profesores).'

    def has_permission(self, request, view):
        return isinstance(request.user, Usuario)
