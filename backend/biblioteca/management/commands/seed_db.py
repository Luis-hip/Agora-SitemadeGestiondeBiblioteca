import datetime
import re

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker

from biblioteca.models import (
    Autor,
    Bibliotecario,
    Categoria,
    ConfiguracionBiblioteca,
    Devolucion,
    Libro,
    Multa,
    Prestamo,
    Usuario,
)

CONTRASENA_PRUEBA = 'Agora2026!'
SEMILLA_ALEATORIA = 20260706

CATEGORIAS = [
    ('Literatura', 'Novelas y obras de ficcion clasica y contemporanea.'),
    ('Ciencia', 'Divulgacion cientifica y ensayos academicos.'),
    ('Historia', 'Obras sobre historia universal y regional.'),
    ('Fantasia', 'Literatura fantastica y de mundos imaginarios.'),
    ('Filosofia', 'Ensayos y tratados filosoficos.'),
    ('Tecnologia', 'Ingenieria de software y desarrollo tecnologico.'),
]

AUTORES = {
    'Gabriel Garcia Marquez': 'Colombiana',
    'George Orwell': 'Britanica',
    'Antoine de Saint-Exupery': 'Francesa',
    'Yuval Noah Harari': 'Israeli',
    'Ray Bradbury': 'Estadounidense',
    'Aldous Huxley': 'Britanica',
    'J.R.R. Tolkien': 'Britanica',
    'J.K. Rowling': 'Britanica',
    'Harper Lee': 'Estadounidense',
    'F. Scott Fitzgerald': 'Estadounidense',
    'Jane Austen': 'Britanica',
    'Fiodor Dostoievski': 'Rusa',
    'J.D. Salinger': 'Estadounidense',
    'Marco Aurelio': 'Romana',
    'Friedrich Nietzsche': 'Alemana',
    'Stephen Hawking': 'Britanica',
    'Carl Sagan': 'Estadounidense',
    'Richard Dawkins': 'Britanica',
    'Jared Diamond': 'Estadounidense',
    'Ana Frank': 'Alemana',
    'Miguel de Cervantes': 'Espanola',
    'Paulo Coelho': 'Brasilena',
    'Robert C. Martin': 'Estadounidense',
    'David Thomas': 'Britanica',
    'Andrew Hunt': 'Estadounidense',
}

LIBROS = [
    ('Cien anos de soledad', '9780307474728', datetime.date(1967, 5, 30), 'Literatura', ['Gabriel Garcia Marquez']),
    ('1984', '9780451524935', datetime.date(1949, 6, 8), 'Literatura', ['George Orwell']),
    ('El Principito', '9780156012195', datetime.date(1943, 4, 6), 'Literatura', ['Antoine de Saint-Exupery']),
    ('Sapiens: De animales a dioses', '9780062316097', datetime.date(2011, 1, 1), 'Historia', ['Yuval Noah Harari']),
    ('Fahrenheit 451', '9781451673319', datetime.date(1953, 10, 19), 'Literatura', ['Ray Bradbury']),
    ('Un mundo feliz', '9780060850524', datetime.date(1932, 1, 1), 'Literatura', ['Aldous Huxley']),
    ('El Hobbit', '9780547928227', datetime.date(1937, 9, 21), 'Fantasia', ['J.R.R. Tolkien']),
    ('Harry Potter y la piedra filosofal', '9780590353427', datetime.date(1997, 6, 26), 'Fantasia', ['J.K. Rowling']),
    ('Matar a un ruisenor', '9780061120084', datetime.date(1960, 7, 11), 'Literatura', ['Harper Lee']),
    ('El gran Gatsby', '9780743273565', datetime.date(1925, 4, 10), 'Literatura', ['F. Scott Fitzgerald']),
    ('Orgullo y prejuicio', '9780141439518', datetime.date(1813, 1, 28), 'Literatura', ['Jane Austen']),
    ('Crimen y castigo', '9780486415871', datetime.date(1866, 1, 1), 'Literatura', ['Fiodor Dostoievski']),
    ('El guardian entre el centeno', '9780316769488', datetime.date(1951, 7, 16), 'Literatura', ['J.D. Salinger']),
    ('Meditaciones', '9780140449334', datetime.date(180, 1, 1), 'Filosofia', ['Marco Aurelio']),
    ('Asi hablo Zaratustra', '9780140441185', datetime.date(1883, 1, 1), 'Filosofia', ['Friedrich Nietzsche']),
    ('Breve historia del tiempo', '9780553380163', datetime.date(1988, 1, 1), 'Ciencia', ['Stephen Hawking']),
    ('Cosmos', '9780345539434', datetime.date(1980, 1, 1), 'Ciencia', ['Carl Sagan']),
    ('El gen egoista', '9780198788607', datetime.date(1976, 1, 1), 'Ciencia', ['Richard Dawkins']),
    ('Armas, germenes y acero', '9780393317558', datetime.date(1997, 3, 1), 'Historia', ['Jared Diamond']),
    ('El diario de Ana Frank', '9780553296983', datetime.date(1947, 6, 25), 'Historia', ['Ana Frank']),
    ('Don Quijote de la Mancha', '9780060934347', datetime.date(1605, 1, 1), 'Literatura', ['Miguel de Cervantes']),
    ('El Alquimista', '9780062315007', datetime.date(1988, 1, 1), 'Literatura', ['Paulo Coelho']),
    ('Homo Deus', '9780062464316', datetime.date(2015, 1, 1), 'Historia', ['Yuval Noah Harari']),
    ('Clean Code', '9780132350884', datetime.date(2008, 8, 1), 'Tecnologia', ['Robert C. Martin']),
    ('The Pragmatic Programmer', '9780135957059', datetime.date(2019, 9, 13), 'Tecnologia', ['David Thomas', 'Andrew Hunt']),
]


def _normalizar(texto):
    tabla = str.maketrans('áéíóúñÁÉÍÓÚÑ', 'aeiounAEIOUN')
    return texto.translate(tabla)


def _slug(texto):
    texto = _normalizar(texto).lower()
    texto = re.sub(r'[^a-z0-9\s]', '', texto)
    return re.sub(r'\s+', '.', texto.strip())


class Command(BaseCommand):
    help = 'Puebla la base de datos con catalogo, usuarios y actividad de prueba (idempotente).'

    @transaction.atomic
    def handle(self, *args, **options):
        self.fake = Faker('es_MX')
        Faker.seed(SEMILLA_ALEATORIA)

        ConfiguracionBiblioteca.cargar()
        categorias = self._crear_categorias()
        autores = self._crear_autores()
        libros = self._crear_libros(categorias, autores)
        estudiantes = self._crear_estudiantes()
        bibliotecarios = self._crear_bibliotecarios()
        self._crear_actividad(estudiantes, bibliotecarios, libros)

        self.stdout.write(self.style.SUCCESS('\nBase de datos poblada correctamente.'))
        self._imprimir_credenciales(estudiantes, bibliotecarios)

    def _crear_categorias(self):
        categorias = {}
        for nombre, descripcion in CATEGORIAS:
            categoria, _ = Categoria.objects.get_or_create(nombre=nombre, defaults={'descripcion': descripcion})
            categorias[nombre] = categoria
        return categorias

    def _crear_autores(self):
        autores = {}
        for nombre, nacionalidad in AUTORES.items():
            autor, _ = Autor.objects.get_or_create(nombre=nombre, defaults={'nacionalidad': nacionalidad})
            autores[nombre] = autor
        return autores

    def _crear_libros(self, categorias, autores):
        libros = []
        for indice, (titulo, isbn, fecha_publicacion, categoria_nombre, nombres_autores) in enumerate(LIBROS):
            libro, creado = Libro.objects.get_or_create(
                isbn=isbn,
                defaults={
                    'titulo': titulo,
                    'fecha_publicacion': fecha_publicacion,
                    'categoria': categorias[categoria_nombre],
                    'disponible': True,
                    'stock': (indice % 4) + 1,
                },
            )
            if creado:
                libro.autores.set([autores[nombre] for nombre in nombres_autores])
            libros.append(libro)
        return libros

    def _crear_estudiantes(self):
        estudiantes = []

        estudiante_fijo, creado = Usuario.objects.get_or_create(
            email='estudiante@agora.edu',
            defaults={
                'matricula': '202312345',
                'nombre': 'Camila Fernandez',
                'telefono': '2221234567',
                'tipo_usuario': Usuario.TipoUsuario.ESTUDIANTE,
            },
        )
        if creado:
            estudiante_fijo.set_password(CONTRASENA_PRUEBA)
            estudiante_fijo.save()
        estudiantes.append(estudiante_fijo)

        for indice in range(1, 5):
            nombre = self.fake.name()
            matricula = f'2023{10000 + indice:05d}'
            email = f'{_slug(nombre)}{indice}@agora.edu'
            telefono = self.fake.numerify('222#######')
            usuario, creado = Usuario.objects.get_or_create(
                matricula=matricula,
                defaults={
                    'email': email,
                    'nombre': nombre,
                    'telefono': telefono,
                    'tipo_usuario': Usuario.TipoUsuario.ESTUDIANTE,
                },
            )
            if creado:
                usuario.set_password(CONTRASENA_PRUEBA)
                usuario.save()
            estudiantes.append(usuario)

        return estudiantes

    def _crear_bibliotecarios(self):
        bibliotecarios = []

        bibliotecario_fijo, creado = Bibliotecario.objects.get_or_create(
            usuario_sistema='bibliotecario',
            defaults={'nombre': 'Luis Hipolito', 'rol': Bibliotecario.Rol.BIBLIOTECARIO},
        )
        if creado:
            bibliotecario_fijo.set_password(CONTRASENA_PRUEBA)
            bibliotecario_fijo.save()
        bibliotecarios.append(bibliotecario_fijo)

        nombre = self.fake.name()
        usuario_sistema = f'admin.{_slug(nombre)}'
        bibliotecario_admin, creado = Bibliotecario.objects.get_or_create(
            usuario_sistema=usuario_sistema,
            defaults={'nombre': nombre, 'rol': Bibliotecario.Rol.ADMIN},
        )
        if creado:
            bibliotecario_admin.set_password(CONTRASENA_PRUEBA)
            bibliotecario_admin.save()
        bibliotecarios.append(bibliotecario_admin)

        return bibliotecarios

    def _crear_prestamo(self, usuario, bibliotecario, libro, dias_transcurridos, estado):
        if Prestamo.objects.filter(usuario=usuario, libro=libro).exists():
            return Prestamo.objects.filter(usuario=usuario, libro=libro).first()

        hoy = timezone.localdate()
        dias_maximos = ConfiguracionBiblioteca.cargar().dias_maximos_prestamo
        fecha_inicio_real = hoy - datetime.timedelta(days=dias_transcurridos)
        fecha_dev_esperada_real = fecha_inicio_real + datetime.timedelta(days=dias_maximos)

        prestamo = Prestamo.objects.create(
            usuario=usuario,
            bibliotecario=bibliotecario,
            libro=libro,
            fecha_dev_esperada=hoy + datetime.timedelta(days=dias_maximos),
        )
        Prestamo.objects.filter(pk=prestamo.pk).update(
            fecha_inicio=fecha_inicio_real, fecha_dev_esperada=fecha_dev_esperada_real, estado=estado,
        )
        prestamo.refresh_from_db()

        if estado in (Prestamo.Estado.ACTIVO, Prestamo.Estado.VENCIDO):
            libro.refresh_from_db()
            nuevo_stock = max(libro.stock - 1, 0)
            Libro.objects.filter(pk=libro.pk).update(stock=nuevo_stock, disponible=nuevo_stock > 0)

        return prestamo

    def _crear_actividad(self, estudiantes, bibliotecarios, libros):
        bibliotecario_principal = bibliotecarios[0]
        disponibles = list(libros)

        # Prestamos activos, dentro del plazo.
        for estudiante in estudiantes[:2]:
            libro = disponibles.pop()
            self._crear_prestamo(estudiante, bibliotecario_principal, libro, dias_transcurridos=3, estado=Prestamo.Estado.ACTIVO)

        # Prestamos vencidos: la fecha limite ya paso y no se han devuelto.
        for estudiante in estudiantes[2:4]:
            libro = disponibles.pop()
            self._crear_prestamo(
                estudiante, bibliotecario_principal, libro, dias_transcurridos=20, estado=Prestamo.Estado.VENCIDO,
            )

        # Prestamo devuelto con atraso: genera una multa pendiente y suspende al usuario (RN-03).
        estudiante_multa = estudiantes[4]
        libro_multa = disponibles.pop()
        prestamo_multa = self._crear_prestamo(
            estudiante_multa, bibliotecario_principal, libro_multa, dias_transcurridos=18, estado=Prestamo.Estado.CERRADO,
        )
        if not Multa.objects.filter(prestamo=prestamo_multa).exists():
            dias_atraso = 4
            fecha_devolucion_real = prestamo_multa.fecha_dev_esperada + datetime.timedelta(days=dias_atraso)
            Devolucion.objects.create(
                prestamo=prestamo_multa, fecha_devolucion=fecha_devolucion_real, condicion='Buen estado',
            )
            libro_multa.refresh_from_db()
            Libro.objects.filter(pk=libro_multa.pk).update(stock=libro_multa.stock + 1, disponible=True)

            tarifa_diaria = ConfiguracionBiblioteca.cargar().tarifa_multa_diaria
            Multa.objects.create(
                prestamo=prestamo_multa,
                usuario=estudiante_multa,
                monto=round(tarifa_diaria * dias_atraso, 2),
                dias_atraso=dias_atraso,
                estado=Multa.Estado.PENDIENTE,
            )
            estudiante_multa.estado = Usuario.Estado.SUSPENDIDO
            estudiante_multa.save(update_fields=['estado'])

    def _imprimir_credenciales(self, estudiantes, bibliotecarios):
        filas = [('CORREO / USUARIO', 'CONTRASENA', 'ROL')]
        for estudiante in estudiantes:
            filas.append((estudiante.email, CONTRASENA_PRUEBA, f'ESTUDIANTE ({estudiante.estado})'))
        for bibliotecario in bibliotecarios:
            filas.append((bibliotecario.usuario_sistema, CONTRASENA_PRUEBA, bibliotecario.rol))

        anchos = [max(len(fila[i]) for fila in filas) + 2 for i in range(3)]

        self.stdout.write(self.style.SUCCESS('\n=== CREDENCIALES DE PRUEBA ==='))
        linea_separadora = '-' * (sum(anchos) + 2)
        print(linea_separadora)
        for indice, fila in enumerate(filas):
            print(''.join(columna.ljust(ancho) for columna, ancho in zip(fila, anchos)))
            if indice == 0:
                print(linea_separadora)
        print(linea_separadora)
