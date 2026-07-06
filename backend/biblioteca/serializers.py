from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password as validar_password_django
from rest_framework import serializers

from .models import (
    Autor,
    Categoria,
    Devolucion,
    Libro,
    Multa,
    Prestamo,
    Usuario,
    matricula_validator,
    telefono_validator,
)
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


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nombre', 'nacionalidad']


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']


class LibroSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    autores = AutorSerializer(many=True, read_only=True)

    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'isbn', 'fecha_publicacion', 'disponible', 'categoria', 'autores']


class PrestamoSerializer(serializers.ModelSerializer):
    libro = LibroSerializer(read_only=True)

    class Meta:
        model = Prestamo
        fields = ['id', 'usuario', 'bibliotecario', 'libro', 'fecha_inicio', 'fecha_dev_esperada', 'estado']
        read_only_fields = fields


class LibroEscrituraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'isbn', 'fecha_publicacion', 'disponible', 'categoria', 'autores']


class PrestamoRequestSerializer(serializers.Serializer):
    libro_id = serializers.IntegerField()
    usuario_id = serializers.IntegerField(required=False)


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'matricula', 'telefono', 'estado', 'tipo_usuario']
        read_only_fields = fields


class MultaSerializer(serializers.ModelSerializer):
    prestamo = PrestamoSerializer(read_only=True)

    class Meta:
        model = Multa
        fields = [
            'id', 'prestamo', 'monto', 'dias_atraso', 'estado',
            'fecha_generacion', 'fecha_pago', 'justificacion_anulacion',
        ]
        read_only_fields = fields


class CalculoMultaRequestSerializer(serializers.Serializer):
    prestamo_id = serializers.IntegerField()
    fecha_devolucion_real = serializers.DateField()


class AnularMultaRequestSerializer(serializers.Serializer):
    justificacion = serializers.CharField(max_length=1000, allow_blank=False)


class UsuarioResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email']
        read_only_fields = fields


class AdminPrestamoSerializer(PrestamoSerializer):
    usuario = UsuarioResumenSerializer(read_only=True)


class AdminMultaSerializer(MultaSerializer):
    prestamo = AdminPrestamoSerializer(read_only=True)


class DevolucionSerializer(serializers.ModelSerializer):
    prestamo = AdminPrestamoSerializer(read_only=True)

    class Meta:
        model = Devolucion
        fields = ['id', 'prestamo', 'fecha_devolucion', 'condicion']
        read_only_fields = fields
