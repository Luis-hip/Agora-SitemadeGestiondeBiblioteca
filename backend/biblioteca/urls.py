from django.urls import path

from .views import LoginView, RegistroUsuarioView

urlpatterns = [
    path('auth/registro/', RegistroUsuarioView.as_view(), name='auth-registro'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
]
