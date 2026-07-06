import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from biblioteca.models import Autor, Bibliotecario, Categoria, Libro, Usuario

CONTRASENA_PRUEBA = 'Agora2026!'


class Command(BaseCommand):
    help = 'Puebla la base de datos con categorias, autores, libros y credenciales de prueba (idempotente).'

    @transaction.atomic
    def handle(self, *args, **options):
        categorias = self._crear_categorias()
        autores = self._crear_autores()
        self._crear_libros(categorias, autores)
        usuario = self._crear_usuario_prueba()
        bibliotecario = self._crear_bibliotecario_prueba()

        self.stdout.write(self.style.SUCCESS('\nBase de datos poblada correctamente.'))
        self.stdout.write(self.style.SUCCESS('\n=== CREDENCIALES DE PRUEBA ==='))
        print(f'Estudiante  -> email: {usuario.email}  password: {CONTRASENA_PRUEBA}')
        print(f'Bibliotecario -> usuario: {bibliotecario.usuario_sistema}  password: {CONTRASENA_PRUEBA}')
        self.stdout.write(self.style.SUCCESS('==============================\n'))

    def _crear_categorias(self):
        datos = [
            ('Literatura', 'Novelas y obras de ficcion clasica y contemporanea.'),
            ('Ciencia', 'Divulgacion cientifica y ensayos academicos.'),
            ('Historia', 'Obras sobre historia universal y regional.'),
        ]
        categorias = {}
        for nombre, descripcion in datos:
            categoria, _ = Categoria.objects.get_or_create(nombre=nombre, defaults={'descripcion': descripcion})
            categorias[nombre] = categoria
        return categorias

    def _crear_autores(self):
        datos = [
            ('Gabriel Garcia Marquez', 'Colombiana'),
            ('George Orwell', 'Britanica'),
            ('Antoine de Saint-Exupery', 'Francesa'),
            ('Yuval Noah Harari', 'Israeli'),
        ]
        autores = {}
        for nombre, nacionalidad in datos:
            autor, _ = Autor.objects.get_or_create(nombre=nombre, defaults={'nacionalidad': nacionalidad})
            autores[nombre] = autor
        return autores

    def _crear_libros(self, categorias, autores):
        datos = [
            {
                'titulo': 'Cien anos de soledad',
                'isbn': '9780307474728',
                'fecha_publicacion': datetime.date(1967, 5, 30),
                'categoria': categorias['Literatura'],
                'autores': ['Gabriel Garcia Marquez'],
            },
            {
                'titulo': '1984',
                'isbn': '9780451524935',
                'fecha_publicacion': datetime.date(1949, 6, 8),
                'categoria': categorias['Literatura'],
                'autores': ['George Orwell'],
            },
            {
                'titulo': 'El Principito',
                'isbn': '9780156012195',
                'fecha_publicacion': datetime.date(1943, 4, 6),
                'categoria': categorias['Literatura'],
                'autores': ['Antoine de Saint-Exupery'],
            },
            {
                'titulo': 'Sapiens: De animales a dioses',
                'isbn': '9780062316097',
                'fecha_publicacion': datetime.date(2011, 1, 1),
                'categoria': categorias['Historia'],
                'autores': ['Yuval Noah Harari'],
            },
        ]
        for entrada in datos:
            libro, creado = Libro.objects.get_or_create(
                isbn=entrada['isbn'],
                defaults={
                    'titulo': entrada['titulo'],
                    'fecha_publicacion': entrada['fecha_publicacion'],
                    'categoria': entrada['categoria'],
                    'disponible': True,
                },
            )
            if creado:
                libro.autores.set([autores[nombre] for nombre in entrada['autores']])

    def _crear_usuario_prueba(self):
        usuario, creado = Usuario.objects.get_or_create(
            email='estudiante@agora.edu',
            defaults={
                'matricula': '202312345',
                'nombre': 'Camila Fernandez',
                'telefono': '2221234567',
                'tipo_usuario': Usuario.TipoUsuario.ESTUDIANTE,
            },
        )
        if creado:
            usuario.set_password(CONTRASENA_PRUEBA)
            usuario.save()
        return usuario

    def _crear_bibliotecario_prueba(self):
        bibliotecario, creado = Bibliotecario.objects.get_or_create(
            usuario_sistema='bibliotecario',
            defaults={
                'nombre': 'Luis Hipolito',
                'rol': Bibliotecario.Rol.BIBLIOTECARIO,
            },
        )
        if creado:
            bibliotecario.set_password(CONTRASENA_PRUEBA)
            bibliotecario.save()
        return bibliotecario
