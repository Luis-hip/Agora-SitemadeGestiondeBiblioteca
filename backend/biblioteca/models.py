from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

matricula_validator = RegexValidator(
    regex=r'^\d{9}$',
    message='La matricula debe contener exactamente 9 digitos numericos.',
)

telefono_validator = RegexValidator(
    regex=r'^\d{7,15}$',
    message='El telefono debe contener solo digitos (7 a 15).',
)


def validar_isbn(value):
    limpio = value.replace('-', '').replace(' ', '')
    if len(limpio) not in (10, 13):
        raise ValidationError('El ISBN debe tener 10 o 13 digitos (guiones y espacios opcionales).')
    if len(limpio) == 13 and not limpio.isdigit():
        raise ValidationError('Un ISBN-13 solo debe contener digitos.')
    if len(limpio) == 10 and not (limpio[:-1].isdigit() and (limpio[-1].isdigit() or limpio[-1].upper() == 'X')):
        raise ValidationError('Un ISBN-10 solo admite digitos, con X como ultimo caracter de verificacion.')


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _crear_usuario(self, email, matricula, nombre, password, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electronico.')
        if not matricula:
            raise ValueError('El usuario debe tener una matricula.')
        email = self.normalize_email(email)
        usuario = self.model(email=email, matricula=matricula, nombre=nombre, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_user(self, email, matricula, nombre, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._crear_usuario(email, matricula, nombre, password, **extra_fields)

    def create_superuser(self, email, matricula, nombre, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._crear_usuario(email, matricula, nombre, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    class Estado(models.TextChoices):
        ACTIVO = 'ACTIVO', 'Activo'
        SUSPENDIDO = 'SUSPENDIDO', 'Suspendido'

    class TipoUsuario(models.TextChoices):
        ESTUDIANTE = 'ESTUDIANTE', 'Estudiante'
        PROFESOR = 'PROFESOR', 'Profesor'

    matricula = models.CharField(max_length=9, unique=True, validators=[matricula_validator])
    nombre = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, validators=[telefono_validator])
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.ACTIVO)
    tipo_usuario = models.CharField(max_length=20, choices=TipoUsuario.choices, default=TipoUsuario.ESTUDIANTE)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField('auth.Group', related_name='usuarios', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='usuarios', blank=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['matricula', 'nombre']

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.nombre} ({self.email})'


class BibliotecarioManager(BaseUserManager):
    use_in_migrations = True

    def _crear_bibliotecario(self, usuario_sistema, nombre, password, **extra_fields):
        if not usuario_sistema:
            raise ValueError('El bibliotecario debe tener una credencial de acceso (usuario_sistema).')
        bibliotecario = self.model(usuario_sistema=usuario_sistema, nombre=nombre, **extra_fields)
        bibliotecario.set_password(password)
        bibliotecario.save(using=self._db)
        return bibliotecario

    def create_user(self, usuario_sistema, nombre, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._crear_bibliotecario(usuario_sistema, nombre, password, **extra_fields)

    def create_superuser(self, usuario_sistema, nombre, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', Bibliotecario.Rol.ADMIN)
        return self._crear_bibliotecario(usuario_sistema, nombre, password, **extra_fields)


class Bibliotecario(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    class Rol(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        BIBLIOTECARIO = 'BIBLIOTECARIO', 'Bibliotecario'

    nombre = models.CharField(max_length=150)
    usuario_sistema = models.CharField(max_length=50, unique=True)
    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.BIBLIOTECARIO)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    groups = models.ManyToManyField('auth.Group', related_name='bibliotecarios', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='bibliotecarios', blank=True)

    objects = BibliotecarioManager()

    USERNAME_FIELD = 'usuario_sistema'
    REQUIRED_FIELDS = ['nombre']

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Bibliotecario'
        verbose_name_plural = 'Bibliotecarios'

    def __str__(self):
        return f'{self.nombre} ({self.usuario_sistema})'


class Autor(TimestampedModel):
    nombre = models.CharField(max_length=200)
    nacionalidad = models.CharField(max_length=100)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    def __str__(self):
        return self.nombre


class Categoria(TimestampedModel):
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField()

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nombre


class Libro(TimestampedModel):
    titulo = models.CharField(max_length=300)
    isbn = models.CharField(max_length=20, unique=True, validators=[validar_isbn])
    fecha_publicacion = models.DateField()
    disponible = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='libros')
    autores = models.ManyToManyField(Autor, related_name='libros')

    class Meta:
        ordering = ['titulo']
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'

    def __str__(self):
        return f'{self.titulo} ({self.isbn})'


class Prestamo(TimestampedModel):
    class Estado(models.TextChoices):
        ACTIVO = 'ACTIVO', 'Activo'
        PROXIMO_A_VENCER = 'PROXIMO_A_VENCER', 'Proximo a vencer'
        CERRADO = 'CERRADO', 'Cerrado'
        VENCIDO = 'VENCIDO', 'Vencido'

    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='prestamos')
    bibliotecario = models.ForeignKey(
        Bibliotecario, on_delete=models.PROTECT, related_name='prestamos_gestionados', null=True, blank=True,
    )
    libro = models.ForeignKey(Libro, on_delete=models.PROTECT, related_name='prestamos')
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_dev_esperada = models.DateField()
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ACTIVO)

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Prestamo'
        verbose_name_plural = 'Prestamos'
        indexes = [
            models.Index(fields=['usuario', 'estado']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['libro'],
                condition=models.Q(estado='ACTIVO'),
                name='unico_prestamo_activo_por_libro',
            ),
            models.CheckConstraint(
                condition=models.Q(fecha_dev_esperada__gt=models.F('fecha_inicio')),
                name='fecha_dev_esperada_posterior_a_fecha_inicio',
            ),
        ]

    def __str__(self):
        return f'Prestamo #{self.pk} - {self.libro} -> {self.usuario}'

    def clean(self):
        super().clean()
        if self.fecha_inicio and self.fecha_dev_esperada and self.fecha_dev_esperada <= self.fecha_inicio:
            raise ValidationError({'fecha_dev_esperada': 'Debe ser estrictamente posterior a la fecha de inicio.'})


class Devolucion(TimestampedModel):
    prestamo = models.OneToOneField(Prestamo, on_delete=models.CASCADE, related_name='devolucion')
    fecha_devolucion = models.DateField()
    condicion = models.CharField(max_length=255)

    class Meta:
        ordering = ['-fecha_devolucion']
        verbose_name = 'Devolucion'
        verbose_name_plural = 'Devoluciones'

    def __str__(self):
        return f'Devolucion de {self.prestamo}'

    def clean(self):
        super().clean()
        if self.prestamo_id and self.fecha_devolucion and self.fecha_devolucion < self.prestamo.fecha_inicio:
            raise ValidationError({'fecha_devolucion': 'No puede ser anterior a la fecha de inicio del prestamo.'})


class Multa(TimestampedModel):
    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        PAGADA = 'PAGADA', 'Pagada'
        ANULADA = 'ANULADA', 'Anulada'

    prestamo = models.ForeignKey(Prestamo, on_delete=models.PROTECT, related_name='multas')
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='multas')
    monto = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    dias_atraso = models.PositiveIntegerField()
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.PENDIENTE)
    fecha_generacion = models.DateField(auto_now_add=True)
    fecha_pago = models.DateField(null=True, blank=True)
    justificacion_anulacion = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-fecha_generacion']
        verbose_name = 'Multa'
        verbose_name_plural = 'Multas'
        constraints = [
            models.UniqueConstraint(
                fields=['prestamo'],
                condition=models.Q(estado='PENDIENTE'),
                name='unica_multa_pendiente_por_prestamo',
            ),
        ]

    def __str__(self):
        return f'Multa #{self.pk} - {self.usuario} (${self.monto})'
