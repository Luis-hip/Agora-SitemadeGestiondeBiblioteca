from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password as validar_password_django
from rest_framework import serializers

from .models import Usuario, matricula_validator, telefono_validator
from .repositories import usuario_repository


class RegistroUsuarioSerializer(serializers.Serializer):
    matricula = serializers.CharField(max_length=9, validators=[matricula_validator])
    nombre = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    telefono = serializers.CharField(max_length=15, validators=[telefono_validator])
    tipo_usuario = serializers.ChoiceField(choices=Usuario.TipoUsuario.choices, default=Usuario.TipoUsuario.ESTUDIANTE)
    password = serializers.CharField(write_only=True)
    password_confirmacion = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if usuario_repository.existe_email(value):
            raise serializers.ValidationError('Este correo ya esta registrado.')
        return value

    def validate_matricula(self, value):
        if usuario_repository.existe_matricula(value):
            raise serializers.ValidationError('Esta matricula ya esta registrada.')
        return value

    def validate_password(self, value):
        try:
            validar_password_django(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(list(exc.messages))
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirmacion'):
            raise serializers.ValidationError({'password_confirmacion': 'Las contrasenas no coinciden.'})
        return attrs


class LoginSerializer(serializers.Serializer):
    identificador = serializers.CharField()
    password = serializers.CharField(write_only=True)
